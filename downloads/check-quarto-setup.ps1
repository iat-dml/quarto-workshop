<#
.SYNOPSIS
  Checks that this Windows computer is ready for the Quarto workshop.

.DESCRIPTION
  Finds every Quarto installation (stand-alone, bundled with RStudio, bundled
  with Positron), checks the version, checks whether a terminal and the VS Code
  Quarto extension can find it, checks R and the R packages used in the
  workshop, and renders a small test document to HTML, DOCX and PDF (Typst).

  Nothing is installed or changed. Each problem is printed with a fix.

  Run it from a PowerShell window:
    powershell -ExecutionPolicy Bypass -File .\check-quarto-setup.ps1

.PARAMETER QuartoPath
  Test this quarto.exe instead of choosing one automatically.

.PARAMETER KioskOnly
  Simulate a fresh ZALF laptop that only has RStudio from the Baramundi Kiosk:
  ignore stand-alone and Positron copies of Quarto (also on PATH) and ignore a
  user-level R_USER or HOME setting.

.PARAMETER SkipRender
  Skip the test render (faster; checks installations only).

.PARAMETER MinVersion
  Lowest Quarto version the workshop materials are tested with.
#>
[CmdletBinding()]
param(
    [string]$QuartoPath,
    [switch]$KioskOnly,
    [switch]$SkipRender,
    [string]$MinVersion = '1.8.25'
)

$ErrorActionPreference = 'Stop'
$results = New-Object System.Collections.Generic.List[object]
$Packages = @('knitr', 'rmarkdown', 'readr', 'dplyr', 'ggplot2', 'plotly', 'DT')

function Add-Result {
    param([string]$Check, [string]$Status, [string]$Detail, [string]$Fix = '')
    $results.Add([pscustomobject]@{ Check = $Check; Status = $Status; Detail = $Detail; Fix = $Fix })
}

function Invoke-Native {
    # Runs a program and returns @{ Code; Output } without letting stderr abort the script.
    param([string]$Exe, [string[]]$Arguments)
    $old = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        $out = & $Exe @Arguments 2>&1 | ForEach-Object { "$_" } | Out-String
        return @{ Code = $LASTEXITCODE; Output = $out.Trim() }
    } catch {
        return @{ Code = 1; Output = "$_" }
    } finally {
        $ErrorActionPreference = $old
    }
}

function Test-NonAscii([string]$s) { return ($s -match '[^\x00-\x7F]') }

function Get-QuartoVersion([string]$exe) {
    $r = Invoke-Native $exe @('--version')
    if ($r.Code -eq 0 -and $r.Output -match '(\d+\.\d+\.\d+)') { return [version]$Matches[1] }
    return $null
}

$pf = $env:ProgramFiles
$la = $env:LOCALAPPDATA
$min = [version]$MinVersion

# Paths a fresh kiosk-only laptop would not have.
$kioskExcluded = @("$la\Programs\Quarto", "$pf\Quarto", "$pf\Positron", "$la\Programs\Positron")
function Test-Excluded([string]$path) {
    if (-not $KioskOnly) { return $false }
    foreach ($e in $kioskExcluded) { if ($path -like "$e*") { return $true } }
    return $false
}

if ($KioskOnly) {
    $env:Path = (($env:Path -split ';') | Where-Object { $_ -and -not (Test-Excluded $_) }) -join ';'
    # A fresh laptop has neither R_USER nor HOME set (Git Bash, for example, sets HOME).
    Remove-Item Env:R_USER -ErrorAction SilentlyContinue
    Remove-Item Env:HOME -ErrorAction SilentlyContinue
    Write-Host "Simulating a kiosk-only laptop: stand-alone/Positron Quarto, R_USER and HOME ignored." -ForegroundColor Yellow
}

# ---------------------------------------------------------------------------
# 1. Quarto installations
# ---------------------------------------------------------------------------
$candidates = [ordered]@{
    'Quarto, all users'               = "$pf\Quarto\bin\quarto.exe"
    'Quarto, per user'                = "$la\Programs\Quarto\bin\quarto.exe"
    'RStudio bundled'                 = "$pf\RStudio\resources\app\bin\quarto\bin\quarto.exe"
    'RStudio bundled (older RStudio)' = "$pf\RStudio\bin\quarto\bin\quarto.exe"
    'Positron bundled, all users'     = "$pf\Positron\resources\app\quarto\bin\quarto.exe"
    'Positron bundled, per user'      = "$la\Programs\Positron\resources\app\quarto\bin\quarto.exe"
}

$found = @()
foreach ($name in $candidates.Keys) {
    $exe = $candidates[$name]
    if ((Test-Path $exe) -and -not (Test-Excluded $exe)) {
        $v = Get-QuartoVersion $exe
        $found += [pscustomobject]@{ Name = $name; Exe = $exe; Version = $v }
        if ($v -and $v -ge $min) {
            Add-Result "Quarto: $name" 'PASS' "$v at $exe"
        } else {
            Add-Result "Quarto: $name" 'WARN' "$v at $exe (older than $MinVersion)" 'Update it, or use another copy listed here.'
        }
    }
}
if ($found.Count -eq 0) {
    Add-Result 'Quarto installed' 'FAIL' 'No Quarto found.' 'Install RStudio from the Baramundi Kiosk (includes Quarto), or the per-user Quarto installer from https://quarto.org/docs/get-started/ (no admin rights needed).'
}

# ---------------------------------------------------------------------------
# 2. Terminal: does `quarto` resolve on PATH?
# ---------------------------------------------------------------------------
$onPath = Get-Command quarto -ErrorAction SilentlyContinue | Select-Object -First 1
$bundledDir = $null
$rstudioQuarto = $candidates['RStudio bundled']
if (Test-Path $rstudioQuarto) { $bundledDir = Split-Path $rstudioQuarto }
if ($onPath) {
    Add-Result 'Terminal finds quarto' 'PASS' $onPath.Source
} else {
    $fix = 'Install the per-user Quarto from quarto.org (it adds itself to PATH).'
    if ($bundledDir) {
        $fix = "Add RStudio's Quarto to your user PATH (no admin needed), then open a new terminal: [Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path','User') + ';$bundledDir', 'User')"
    }
    Add-Result 'Terminal finds quarto' 'WARN' "'quarto' is not on PATH. RStudio still works; terminals and VS Code do not." $fix
}

# ---------------------------------------------------------------------------
# 3. VS Code Quarto extension
# ---------------------------------------------------------------------------
$codeExe = @("$la\Programs\Microsoft VS Code\Code.exe", "$pf\Microsoft VS Code\Code.exe") | Where-Object { Test-Path $_ } | Select-Object -First 1
if ($codeExe) {
    $settingsFile = "$env:APPDATA\Code\User\settings.json"
    $settingPath = $null
    if (Test-Path $settingsFile) {
        $raw = Get-Content $settingsFile -Raw
        if ($raw -match '"quarto\.path"\s*:\s*"([^"]+)"') { $settingPath = $Matches[1] -replace '\\\\', '\' }
    }
    # The extension (v1.138) looks at quarto.path, then PATH, then these folders.
    $extFallback = @("$pf\Quarto\bin", "$la\Programs\Quarto\bin", "$pf\RStudio\bin\quarto\bin")
    $fallbackHit = $extFallback | Where-Object { (Test-Path "$_\quarto.exe") -and -not (Test-Excluded $_) } | Select-Object -First 1
    if ($settingPath -and (Test-Path $settingPath)) {
        Add-Result 'VS Code finds Quarto' 'PASS' "quarto.path = $settingPath"
    } elseif ($settingPath) {
        Add-Result 'VS Code finds Quarto' 'FAIL' "quarto.path points to a missing file: $settingPath" 'Correct the quarto.path setting in VS Code.'
    } elseif ($onPath) {
        Add-Result 'VS Code finds Quarto' 'PASS' "via PATH: $($onPath.Source)"
    } elseif ($fallbackHit) {
        Add-Result 'VS Code finds Quarto' 'PASS' "via extension default folder: $fallbackHit"
    } else {
        $fix = 'Install the per-user Quarto from quarto.org.'
        if ($bundledDir) {
            $jsonPath = ($rstudioQuarto -replace '\\', '\\')
            $fix = "In VS Code settings.json add:  `"quarto.path`": `"$jsonPath`""
        }
        Add-Result 'VS Code finds Quarto' 'FAIL' "The Quarto extension does not look in RStudio's current folder (resources\app\bin\quarto)." $fix
    }
} else {
    Add-Result 'VS Code' 'INFO' 'VS Code not installed; skipped.'
}

# ---------------------------------------------------------------------------
# 4. Positron
# ---------------------------------------------------------------------------
$positron = $found | Where-Object { $_.Name -like 'Positron*' } | Select-Object -First 1
if ($positron) {
    Add-Result 'Positron' 'PASS' "Bundles Quarto $($positron.Version); works inside Positron without further setup."
} elseif (-not $KioskOnly) {
    Add-Result 'Positron' 'INFO' 'Positron not installed; skipped.'
}

# ---------------------------------------------------------------------------
# 5. Folder names (OneDrive paths with umlauts break R and some extensions)
# ---------------------------------------------------------------------------
$docs = [Environment]::GetFolderPath('MyDocuments')
if (Test-NonAscii $docs) {
    Add-Result 'Documents folder' 'WARN' 'Your Documents folder path contains non-ASCII characters, which is typical of ZALF OneDrive folders.' 'Keep workshop projects in a plain folder such as C:\Users\<you>\quarto-workshop, not under OneDrive.'
} else {
    Add-Result 'Documents folder' 'PASS' $docs
}

# ---------------------------------------------------------------------------
# 6. R, R home and packages
# ---------------------------------------------------------------------------
$rscript = (Get-Command Rscript -ErrorAction SilentlyContinue | Select-Object -First 1).Source
if (-not $rscript) {
    foreach ($key in @('HKLM:\SOFTWARE\R-core\R', 'HKCU:\SOFTWARE\R-core\R')) {
        $ip = (Get-ItemProperty $key -ErrorAction SilentlyContinue).InstallPath
        if ($ip -and (Test-Path "$ip\bin\Rscript.exe")) { $rscript = "$ip\bin\Rscript.exe"; break }
    }
}
if (-not $rscript) {
    $rscript = Get-ChildItem "$pf\R\R-*\bin\Rscript.exe" -ErrorAction SilentlyContinue | Sort-Object FullName -Descending | Select-Object -First 1 -ExpandProperty FullName
}

if (-not $rscript) {
    Add-Result 'R installed' 'FAIL' 'R not found.' 'Install R from the Baramundi Kiosk (or https://cran.r-project.org).'
} else {
    $rv = Invoke-Native $rscript @('-e', 'cat(R.version$major, R.version$minor, sep=''.'')')
    Add-Result 'R installed' 'PASS' "R $($rv.Output) at $rscript"

    $homeCheck = Invoke-Native $rscript @('-e', "tryCatch({ dir.exists(path.expand('~/opt/pandoc')); cat('OK') }, error = function(e) cat('ERROR:', conditionMessage(e)))")
    if ($homeCheck.Output -match 'OK$') {
        Add-Result 'R home folder' 'PASS' 'R can read its home folder.'
    } else {
        Add-Result 'R home folder' 'FAIL' "R cannot handle its home folder path ($($homeCheck.Output)). Every R chunk render will fail." "Set R_USER to a plain path, then restart RStudio/VS Code/Positron: [Environment]::SetEnvironmentVariable('R_USER', `$env:USERPROFILE, 'User')"
    }

    $pkgList = "c('" + ($Packages -join "','") + "')"
    $pk = Invoke-Native $rscript @('-e', "p <- $pkgList; m <- p[!vapply(p, requireNamespace, logical(1), quietly = TRUE)]; cat('MISSING:', paste(m, collapse = ','))")
    if ($pk.Output -match 'MISSING:\s*(\S*)\s*$') {
        $missing = $Matches[1]
        if ($missing) {
            $quoted = "'" + ($missing -replace ',', "', '") + "'"
            Add-Result 'R packages' 'FAIL' "Missing: $missing" "In R run: install.packages(c($quoted))"
        } else {
            Add-Result 'R packages' 'PASS' ($Packages -join ', ')
        }
    } else {
        Add-Result 'R packages' 'WARN' "Could not check packages: $($pk.Output)"
    }
}

# ---------------------------------------------------------------------------
# 7. Test render
# ---------------------------------------------------------------------------
$selected = $null
if ($QuartoPath) {
    if (Test-Path $QuartoPath) { $selected = $QuartoPath } else { Add-Result 'Selected Quarto' 'FAIL' "Not found: $QuartoPath" }
} elseif ($KioskOnly) {
    $selected = ($found | Where-Object { $_.Name -like 'RStudio*' } | Select-Object -First 1).Exe
} elseif ($onPath) {
    $selected = $onPath.Source
} elseif ($found.Count -gt 0) {
    $selected = ($found | Sort-Object Version -Descending | Select-Object -First 1).Exe
}

if ($selected -and -not $SkipRender) {
    $sv = Get-QuartoVersion $selected
    Add-Result 'Quarto used for test render' 'INFO' "$sv at $selected"

    $work = Join-Path $env:TEMP 'quarto-setup-check'
    if (Test-Path $work) { Remove-Item $work -Recurse -Force }
    New-Item -ItemType Directory -Path $work | Out-Null

    $qmd = @'
---
title: "Workshop setup check"
bibliography: refs.bib
execute:
  echo: false
---

```{r}
#| label: setup
x <- c(3, 5, 8, 13)
```

The mean of the test values is `r mean(x)`.

```{r}
#| label: fig-test
#| fig-cap: "A test figure."
plot(x, type = "b")
```

@fig-test shows the values, rendered with Quarto [@quarto].
'@
    $bib = @'
@software{quarto,
  author = {Allaire, J. J. and Teague, Charles and Scheidegger, Carlos and Xie, Yihui and Dervieux, Christophe},
  title  = {Quarto},
  year   = {2022},
  doi    = {10.5281/zenodo.5960048}
}
'@
    Set-Content -Path (Join-Path $work 'smoke.qmd') -Value $qmd -Encoding ASCII
    Set-Content -Path (Join-Path $work 'refs.bib') -Value $bib -Encoding ASCII

    Push-Location $work
    try {
        foreach ($t in @(@{ To = 'html'; Out = 'smoke.html' }, @{ To = 'docx'; Out = 'smoke.docx' }, @{ To = 'typst'; Out = 'smoke.pdf' })) {
            $r = Invoke-Native $selected @('render', 'smoke.qmd', '--to', $t.To)
            if ($r.Code -eq 0 -and (Test-Path (Join-Path $work $t.Out))) {
                Add-Result "Render to $($t.To)" 'PASS' $t.Out
            } else {
                $tail = (($r.Output -split "`n") | Select-Object -Last 4) -join ' '
                Add-Result "Render to $($t.To)" 'FAIL' $tail 'See the messages above; ask us at the workshop.'
            }
        }
    } finally {
        Pop-Location
    }
}

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
Write-Host ''
foreach ($r in $results) {
    $colour = switch ($r.Status) { 'PASS' { 'Green' } 'WARN' { 'Yellow' } 'FAIL' { 'Red' } default { 'Gray' } }
    Write-Host ('[{0}] {1}: {2}' -f $r.Status, $r.Check, $r.Detail) -ForegroundColor $colour
}
$fixes = $results | Where-Object { $_.Fix }
if ($fixes) {
    Write-Host ''
    Write-Host 'How to fix:' -ForegroundColor Cyan
    foreach ($f in $fixes) { Write-Host ("- {0}: {1}" -f $f.Check, $f.Fix) }
}
$failed = @($results | Where-Object { $_.Status -eq 'FAIL' }).Count
Write-Host ''
if ($failed -gt 0) {
    Write-Host "$failed check(s) failed." -ForegroundColor Red
    exit 1
}
Write-Host 'Ready for the workshop.' -ForegroundColor Green
exit 0

# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow>=10", "imageio-ffmpeg>=0.5", "pyyaml>=6"]
# ///
"""Build a karaoke-style practice video of the pitch talking points.

Reads the timings table in cue-sheet.md, lays each scene's talking point out
on screen and fills in the words as they should be spoken, so the practice
video lines up with the pitch video scene by scene. The pitch video's audio
is copied in, so the musical cues are the same as on the day.

Usage (from this folder):
    uv run --script build-practice-video.py              # full video
    uv run --script build-practice-video.py --still 1:52 # one frame as PNG
    uv run --script build-practice-video.py --help

uv installs Pillow, PyYAML and imageio-ffmpeg (which ships its own ffmpeg
binary) on first run, so nothing else needs to be installed.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

import imageio_ffmpeg
import yaml
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
REPO = HERE.parent

# Video geometry
W, H = 1920, 1080
MARGIN_X = 120

# Timing: when the words start and stop filling within a scene (seconds)
LEAD = 0.3   # pause after the cut before the first word
TAIL = 0.6   # breathing room before the next cut
# Slowest fill rate, in weight units per second (about 1.8 words a second).
# A short talking point in a long scene fills at this pace and then waits,
# instead of crawling across the whole scene.
SLOW_UNITS_PER_SEC = 2.9

# Pacing thresholds for the report, in words per second of speaking time
PACE_FAST = 2.6     # about 155 words a minute: quick for a pitch
PACE_TOO_FAST = 3.1 # about 185 words a minute: hard to say clearly


# --------------------------------------------------------------------------
# Cue sheet
# --------------------------------------------------------------------------

@dataclass
class Scene:
    start: float
    name: str
    caption: str
    text: str
    end: float = 0.0
    words: list = field(default_factory=list)   # (token, t0, t1); "\n" = break


def parse_time(value: str) -> float:
    m = re.fullmatch(r"\s*(\d+):(\d{1,2}(?:\.\d+)?)\s*", value)
    if not m:
        raise ValueError(f"Cannot read time {value!r}; use m:ss or m:ss.s")
    return int(m.group(1)) * 60 + float(m.group(2))


def fmt_time(seconds: float) -> str:
    seconds = max(0, int(seconds))
    return f"{seconds // 60}:{seconds % 60:02d}"


def clean_cell(cell: str) -> str:
    cell = cell.replace("**", "").replace("`", "").strip()
    return cell


def read_cue_sheet(path: Path) -> list[Scene]:
    lines = path.read_text(encoding="utf-8").splitlines()
    header_idx = next(
        (i for i, ln in enumerate(lines) if re.match(r"\s*\|\s*Time\s*\|", ln)), None
    )
    if header_idx is None:
        sys.exit(f"No table with a 'Time' column found in {path.name}")

    def cells(ln: str) -> list[str]:
        return [c.strip() for c in ln.strip().strip("|").split("|")]

    header = [h.lower() for h in cells(lines[header_idx])]

    def col(*names: str) -> int:
        for i, h in enumerate(header):
            if any(n in h for n in names):
                return i
        sys.exit(f"Cue sheet table needs a column named like {names[0]!r}")

    c_time, c_scene = col("time"), col("scene")
    c_caption, c_talk = col("caption"), col("talking")

    scenes: list[Scene] = []
    for ln in lines[header_idx + 2:]:
        if not ln.strip().startswith("|"):
            break
        row = cells(ln)
        if len(row) <= max(c_time, c_scene, c_caption, c_talk):
            continue
        scenes.append(Scene(
            start=parse_time(row[c_time]),
            name=clean_cell(row[c_scene]),
            caption=clean_cell(row[c_caption]),
            text=clean_cell(row[c_talk]),
        ))
    if not scenes:
        sys.exit("The cue sheet table has no rows")
    for a, b in zip(scenes, scenes[1:]):
        if b.start <= a.start:
            sys.exit(f"Scene times must increase: {a.name!r} then {b.name!r}")
    return scenes


# --------------------------------------------------------------------------
# Timing
# --------------------------------------------------------------------------

def tokenise(text: str) -> list[str]:
    text = re.sub(r"<br\s*/?>", " \n ", text, flags=re.I)
    return [t for t in re.split(r"[ \t]+", text) if t]


def is_spoken(token: str) -> bool:
    """False for markers such as ① that are read silently."""
    return any(ch.isalpha() or ch.isascii() and ch.isdigit() for ch in token)


def word_weight(token: str) -> tuple[float, float]:
    """Relative time to say a word, and the pause after it."""
    if not is_spoken(token):
        return 0.3, 0.0   # a marker like ① gets a beat, not a word
    letters = len(re.sub(r"[^\w]", "", token))
    say = 0.55 + 0.11 * letters
    pause = 0.0
    if token.endswith((",", ";", ":")):
        pause = 0.5
    elif token.endswith((".", "?", "!")):
        pause = 0.9
    return say, pause


def time_words(scene: Scene) -> None:
    tokens = tokenise(scene.text)
    weights = [word_weight(t) if t != "\n" else (0.0, 0.0) for t in tokens]
    # The pause after the last word does not need room
    total = sum(s + p for s, p in weights) - (weights[-1][1] if weights else 0)
    t0 = scene.start + LEAD
    avail = max(0.5, scene.end - TAIL - t0)
    span = min(avail, total / SLOW_UNITS_PER_SEC) if total else 0
    scale = span / total if total else 0
    t = t0
    scene.words = []
    for tok, (say, pause) in zip(tokens, weights):
        scene.words.append((tok, t, t + say * scale))
        t += (say + pause) * scale


def pacing_report(scenes: list[Scene]) -> None:
    print("\nPacing (words per second of speaking time)")
    print(f"{'Time':>5}  {'Scene':<24}{'Words':>6}{'Secs':>6}{'W/s':>6}  Note")
    for s in scenes:
        n = sum(1 for w in s.words if w[0] != "\n" and is_spoken(w[0]))
        secs = max(0.1, s.end - s.start - LEAD - TAIL)
        wps = n / secs
        note = ""
        if wps > PACE_TOO_FAST:
            keep = int(secs * PACE_FAST)
            note = f"too fast: aim for about {keep} words"
        elif wps > PACE_FAST:
            note = "fast"
        print(f"{fmt_time(s.start):>5}  {s.name[:23]:<24}{n:>6}{secs:>6.1f}{wps:>6.1f}  {note}")
    print()


# --------------------------------------------------------------------------
# Look: brand colours and fonts
# --------------------------------------------------------------------------

def brand_colours() -> dict[str, str]:
    colours = {   # fallback if dark-brand.yml cannot be read
        "night": "#0F1024", "night-2": "#171936", "night-3": "#23254A",
        "paper": "#F2EBE0", "paper-2": "#C8C2BA", "muted": "#8A8499",
        "indigo": "#A899FF", "amber": "#F2C56B",
    }
    try:
        brand = yaml.safe_load((REPO / "dark-brand.yml").read_text(encoding="utf-8"))
        colours.update(brand["color"]["palette"])
    except Exception as exc:  # noqa: BLE001
        print(f"Using built-in colours ({exc})")
    return colours


FONT_DIRS = [
    Path.home() / "AppData/Local/Microsoft/Windows/Fonts",
    Path("C:/Windows/Fonts"),
    Path("/Library/Fonts"), Path.home() / "Library/Fonts",
    Path("/usr/share/fonts"), Path.home() / ".fonts",
]


def find_font(*names: str) -> str:
    for name in names:
        for d in FONT_DIRS:
            hits = list(d.rglob(name)) if d.exists() else []
            if hits:
                return str(hits[0])
    sys.exit(f"None of these fonts is installed: {', '.join(names)}")


class Fonts:
    def __init__(self) -> None:
        self.text_path = find_font("IBMPlexSans-SemiBold.ttf", "seguisb.ttf",
                                   "DejaVuSans-Bold.ttf", "Arial.ttf")
        self.ui_path = find_font("IBMPlexSans-Regular.ttf", "segoeui.ttf",
                                 "DejaVuSans.ttf", "Arial.ttf")
        self.mono_path = find_font("IBMPlexMono-Regular.ttf", "consola.ttf",
                                   "DejaVuSansMono.ttf", "Courier New.ttf")
        try:
            self.symbol_path = find_font("seguisym.ttf", "DejaVuSans.ttf")
        except SystemExit:
            self.symbol_path = self.text_path
        self._cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}

    def get(self, path: str, size: int) -> ImageFont.FreeTypeFont:
        key = (path, size)
        if key not in self._cache:
            self._cache[key] = ImageFont.truetype(path, size)
        return self._cache[key]

    def for_token(self, token: str, size: int) -> ImageFont.FreeTypeFont:
        """Main text font, or the symbol font when a glyph (e.g. ①) is missing."""
        main = self.get(self.text_path, size)
        if all(has_glyph(main, c) for c in token):
            return main
        return self.get(self.symbol_path, size)


_notdef: dict[int, bytes] = {}


def has_glyph(font: ImageFont.FreeTypeFont, char: str) -> bool:
    if char.isascii():
        return True
    key = id(font)
    if key not in _notdef:
        _notdef[key] = bytes(font.getmask("\uffff"))
    return bytes(font.getmask(char)) != _notdef[key]


# --------------------------------------------------------------------------
# Layout and drawing
# --------------------------------------------------------------------------

TEXT_TOP, TEXT_BOTTOM = 230, 900   # area for the talking point
HEADER_BASELINE = 90


@dataclass
class Layout:
    boxes: list          # per token: (x, y, w, h) or None for line breaks
    dim: Image.Image     # whole frame, words in the not-yet-said colour
    said: Image.Image    # words in the said colour
    now: Image.Image     # words in the being-said colour


def layout_words(scene: Scene, fonts: Fonts, size: int):
    """Wrap tokens into centred lines; return boxes or None if it does not fit."""
    max_w = W - 2 * MARGIN_X
    line_h = int(size * 1.42)
    space = fonts.get(fonts.text_path, size).getlength(" ")
    lines: list[list[tuple[int, float]]] = [[]]
    widths = [0.0]
    for i, (tok, _, _) in enumerate(scene.words):
        if tok == "\n":
            lines.append([]); widths.append(0.0)
            continue
        w = fonts.for_token(tok, size).getlength(tok)
        extra = (space if lines[-1] else 0) + w
        if lines[-1] and widths[-1] + extra > max_w:
            lines.append([]); widths.append(0.0)
            extra = w
        lines[-1].append((i, w))
        widths[-1] += extra
    total_h = line_h * len(lines)
    if total_h > TEXT_BOTTOM - TEXT_TOP:
        return None
    boxes: list = [None] * len(scene.words)
    y = TEXT_TOP + (TEXT_BOTTOM - TEXT_TOP - total_h) // 2
    for line, lw in zip(lines, widths):
        x = (W - lw) / 2
        for i, w in line:
            boxes[i] = (int(x), y, int(w) + 1, line_h)
            x += w + space
        y += line_h
    return boxes


def build_layout(scene: Scene, idx: int, scenes: list[Scene], fonts: Fonts,
                 c: dict[str, str]) -> Layout:
    size = 76
    boxes = layout_words(scene, fonts, size)
    while boxes is None and size > 30:
        size -= 4
        boxes = layout_words(scene, fonts, size)

    # Static background shared by all three colour layers
    base = Image.new("RGB", (W, H), c["night"])
    d = ImageDraw.Draw(base)
    ui = fonts.get(fonts.ui_path, 32)
    small = fonts.get(fonts.ui_path, 26)
    d.text((MARGIN_X, HEADER_BASELINE), f"Scene {idx + 1} of {len(scenes)}", font=ui,
           fill=c["muted"], anchor="ls")
    d.text((MARGIN_X + 260, HEADER_BASELINE), scene.name, font=ui, fill=c["paper-2"],
           anchor="ls")
    caption = scene.caption if scene.caption.lower() != "none" else "no caption"
    if re.fullmatch(r'"[^"]*"', caption):
        caption = caption[1:-1]
    caption = re.sub(r'"([^"]*)"', "“\\1”", caption)
    d.text((MARGIN_X, 108), f"On screen: {caption}", font=small, fill=c["muted"])
    if idx + 1 < len(scenes):
        nxt = scenes[idx + 1]
        preview = " ".join(t for t, _, _ in nxt.words[:9] if t != "\n")
        if len(nxt.words) > 9:
            preview += " …"
        d.text((MARGIN_X, 952), f"Next at {fmt_time(nxt.start)}, {nxt.name}:",
               font=small, fill=c["muted"])
        d.text((MARGIN_X + 20 + small.getlength(f"Next at {fmt_time(nxt.start)}, {nxt.name}:"),
                952), preview, font=small, fill=c["paper-2"])

    layers = []
    for colour in (c["muted"], c["paper"], c["amber"]):
        img = base.copy()
        dd = ImageDraw.Draw(img)
        for (tok, _, _), box in zip(scene.words, boxes):
            if box is None:
                continue
            font = fonts.for_token(tok, size)
            # Baseline at about 72 % of the line height
            dd.text((box[0], box[1] + int(box[3] * 0.74)), tok, font=font,
                    fill=colour, anchor="ls")
        layers.append(img)
    return Layout(boxes=boxes, dim=layers[0], said=layers[1], now=layers[2])


def draw_frame(t: float, scene: Scene, lay: Layout, total: float, scenes: list[Scene],
               fonts: Fonts, c: dict[str, str]) -> Image.Image:
    frame = lay.dim.copy()
    for (tok, t0, t1), box in zip(scene.words, lay.boxes):
        if box is None or t < t0:
            continue
        x, y, w, h = box
        if t >= t1:
            frame.paste(lay.said.crop((x, y, x + w, y + h)), (x, y))
        else:
            # Word being said: wipe the highlight colour across it
            fw = max(1, int(w * (t - t0) / max(1e-6, t1 - t0)))
            frame.paste(lay.now.crop((x, y, x + w, y + h)), (x, y))
            frame.paste(lay.dim.crop((x + fw, y, x + w, y + h)), (x + fw, y))

    d = ImageDraw.Draw(frame)
    mono = fonts.get(fonts.mono_path, 32)
    tc = f"{fmt_time(t)} / {fmt_time(total)}"
    d.text((W - MARGIN_X, HEADER_BASELINE), tc, font=mono, fill=c["paper-2"], anchor="rs")

    # Scene progress
    y = 168
    d.rectangle([MARGIN_X, y, W - MARGIN_X, y + 5], fill=c["night-3"])
    frac = (t - scene.start) / max(1e-6, scene.end - scene.start)
    d.rectangle([MARGIN_X, y, MARGIN_X + int((W - 2 * MARGIN_X) * min(1, frac)), y + 5],
                fill=c["indigo"])

    # Whole-video progress with a tick at each scene start
    y = 1022
    d.rectangle([MARGIN_X, y, W - MARGIN_X, y + 3], fill=c["night-3"])
    span = W - 2 * MARGIN_X
    d.rectangle([MARGIN_X, y, MARGIN_X + int(span * t / total), y + 3], fill=c["muted"])
    for s in scenes[1:]:
        x = MARGIN_X + int(span * s.start / total)
        d.rectangle([x - 1, y - 6, x + 1, y + 9], fill=c["paper-2"])

    # Countdown in the last three seconds of a scene
    left = scene.end - t
    if 0 < left <= 3 and scene is not scenes[-1]:
        small = fonts.get(fonts.ui_path, 26)
        d.text((W - MARGIN_X, 952), f"next scene in {int(left) + 1}", font=small,
               fill=c["amber"], anchor="ra")
    return frame


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def find_video(arg: str | None) -> Path | None:
    if arg:
        return Path(arg)
    for name in ("a-year-in-research-quarto-workshop-pitch.mp4", "pitch-video.mp4"):
        if (HERE / name).exists():
            return HERE / name
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--cue-sheet", default=str(HERE / "cue-sheet.md"))
    ap.add_argument("--video", help="pitch video, for its length and soundtrack")
    ap.add_argument("--output", help="default practice-video.mp4, or "
                    "practice-video-side-by-side.mp4 with --side-by-side")
    ap.add_argument("--side-by-side", action="store_true",
                    help="put the pitch video on the left and the talking points on the right")
    ap.add_argument("--no-audio", action="store_true", help="leave out the soundtrack")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--still", metavar="M:SS", help="write one frame to practice-still.png")
    args = ap.parse_args()

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    scenes = read_cue_sheet(Path(args.cue_sheet))
    video = find_video(args.video)
    if video and video.exists():
        _, total = imageio_ffmpeg.count_frames_and_secs(str(video))
    else:
        print("Pitch video not found: using 2:55 and no soundtrack")
        video, total = None, 175.0
    if scenes[-1].start >= total:
        sys.exit(f"Last scene starts at {fmt_time(scenes[-1].start)}, after the video ends")
    for a, b in zip(scenes, scenes[1:]):
        a.end = b.start
    scenes[-1].end = total
    for s in scenes:
        time_words(s)
    pacing_report(scenes)

    colours = brand_colours()
    fonts = Fonts()
    layouts = [build_layout(s, i, scenes, fonts, colours) for i, s in enumerate(scenes)]

    def scene_at(t: float) -> int:
        idx = 0
        for i, s in enumerate(scenes):
            if t >= s.start:
                idx = i
        return idx

    if args.still:
        t = parse_time(args.still)
        i = scene_at(t)
        out = HERE / "practice-still.png"
        draw_frame(t, scenes[i], layouts[i], total, scenes, fonts, colours).save(out)
        print(f"Wrote {out}")
        return

    if args.side_by_side and not video:
        sys.exit("--side-by-side needs the pitch video")
    output = args.output or str(
        HERE / ("practice-video-side-by-side.mp4" if args.side_by_side else "practice-video.mp4"))

    n_frames = round(total * args.fps)
    cmd = [ffmpeg, "-y", "-v", "error", "-stats",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(args.fps), "-i", "-"]
    if video:
        cmd += ["-i", str(video)]
    if args.side_by_side:
        # Pitch video left, talking points right, one frame clock for both
        cmd += ["-filter_complex",
                f"[1:v]scale={W}:{H},fps={args.fps},setpts=PTS-STARTPTS[pitch];"
                f"[0:v]setpts=PTS-STARTPTS[talk];[pitch][talk]hstack=inputs=2[v]",
                "-map", "[v]"]
    else:
        cmd += ["-map", "0:v"]
    if video and not args.no_audio:
        cmd += ["-map", "1:a?", "-c:a", "copy"]
    tune = [] if args.side_by_side else ["-tune", "stillimage"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "20", *tune,
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-t", f"{total:.3f}",
            output]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    try:
        for f in range(n_frames):
            t = f / args.fps
            i = scene_at(t)
            frame = draw_frame(t, scenes[i], layouts[i], total, scenes, fonts, colours)
            proc.stdin.write(frame.tobytes())
    finally:
        proc.stdin.close()
        proc.wait()
    if proc.returncode:
        sys.exit(f"ffmpeg failed with code {proc.returncode}")
    print(f"\nWrote {output} ({fmt_time(total)}, {n_frames} frames)")


if __name__ == "__main__":
    main()

# /// script
# requires-python = ">=3.10"
# dependencies = ["playwright>=1.48", "pillow>=10", "pyyaml>=6"]
# ///
"""Record the two screen recordings shown on the ZALF deck's opening slides.

    open-slides.gif  The home page, a click on "View as presentation", and the
                     deck opening on the title slide and then the plan.
    copy-code.gif    A code block on the Step 2 slide, its copy button
                     appearing on hover, and a click that copies the code.

Both are recorded from the local build in _site/, so render first. From the
repo root:

    QUARTO_PROFILE=website quarto render index.qmd
    QUARTO_PROFILE=website quarto render slides/zalf-2026.qmd
    uv run --script _screencasts/record-screencasts.py

The GIFs are written to assets/screencasts/. Render the deck once more
afterwards so _site/ picks them up.

Playwright drives the installed Microsoft Edge (channel "msedge"), so no
browser is downloaded. A headless browser shows neither a mouse pointer nor
an address bar, so both are drawn onto each frame here. The address bar
shows the public URL rather than the local file path.
"""

from __future__ import annotations

import io
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import Page, sync_playwright

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SITE = REPO / "_site"
OUT = REPO / "assets" / "screencasts"

LOCAL_ROOT = SITE.as_uri() + "/"
PUBLIC_ROOT = "iat-dml.github.io/quarto-workshop/"

PALETTE = yaml.safe_load((REPO / "_brand.yml").read_text(encoding="utf-8"))["color"]["palette"]

# Browser chrome drawn above the page. Neutral greys, like a light browser theme.
BAR_H = 52
BAR_BG = (243, 243, 243)
BAR_RULE = (220, 220, 220)
PILL_BG = (255, 255, 255)
URL_HOST = (31, 31, 31)
URL_PATH = (110, 110, 110)

FRAME_MS = 50  # one frame of pointer movement


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for name in ("segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def hex_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


GREEN = hex_rgb(PALETTE["green"])
FOREST = hex_rgb(PALETTE["forest"])


def ease(t: float) -> float:
    """Ease in and out, so the pointer starts and stops gently."""
    return t * t * (3 - 2 * t)


class Recorder:
    """Collects frames from a page, with a drawn pointer and optional chrome."""

    def __init__(self, page: Page, chrome: bool, crop: tuple[int, int, int, int] | None = None):
        self.page = page
        self.chrome = chrome
        self.crop = crop
        self.x, self.y = 0.0, 0.0
        self.pointer_visible = True
        self.frames: list[tuple[Image.Image, int]] = []
        self.url_font = font(19)
        self.key_font = font(30)

    # -- frame composition ------------------------------------------------
    def display_url(self) -> str:
        url = self.page.url
        if url.startswith(LOCAL_ROOT):
            url = PUBLIC_ROOT + url[len(LOCAL_ROOT):]
        return url.replace("index.html", "")

    def draw_chrome(self, shot: Image.Image) -> Image.Image:
        w, h = shot.size
        frame = Image.new("RGB", (w, h + BAR_H), BAR_BG)
        frame.paste(shot, (0, BAR_H))
        d = ImageDraw.Draw(frame)
        d.line([(0, BAR_H - 1), (w, BAR_H - 1)], fill=BAR_RULE, width=1)
        d.rounded_rectangle([16, 9, w - 16, BAR_H - 10], radius=17, fill=PILL_BG, outline=BAR_RULE)
        url = self.display_url()
        host, _, path = url.partition("/")
        x, y = 36, BAR_H / 2
        d.text((x, y), host, font=self.url_font, fill=URL_HOST, anchor="lm")
        x += d.textlength(host, font=self.url_font)
        d.text((x, y), "/" + path, font=self.url_font, fill=URL_PATH, anchor="lm")
        return frame

    def draw_pointer(self, frame: Image.Image, x: float, y: float, pressed: bool) -> None:
        d = ImageDraw.Draw(frame)
        if pressed:
            for r, width in ((22, 3), (30, 2)):
                d.ellipse([x - r, y - r, x + r, y + r], outline=GREEN, width=width)
        s = 1.35
        arrow = [(0, 0), (0, 17), (4.2, 13), (7, 19.5), (9.6, 18.4), (6.9, 12.2), (12.5, 12.2)]
        pts = [(x + px * s, y + py * s) for px, py in arrow]
        d.polygon(pts, fill=(255, 255, 255))
        inner = [(x + px * s * 0.82 + 1.2, y + py * s * 0.82 + 2.2) for px, py in arrow]
        d.polygon(inner, fill=(20, 20, 20))

    def draw_key(self, frame: Image.Image, label: str) -> None:
        d = ImageDraw.Draw(frame)
        # Bottom centre, above the deck's footer and clear of its menu button.
        w, h = frame.size
        box = [w / 2 - 38, h - 150, w / 2 + 38, h - 86]
        d.rounded_rectangle(box, radius=12, fill=(255, 255, 255), outline=FOREST, width=3)
        d.text(((box[0] + box[2]) / 2, (box[1] + box[3]) / 2 - 2), label,
               font=self.key_font, fill=FOREST, anchor="mm")

    def snap(self, ms: int, pressed: bool = False, key: str | None = None) -> None:
        shot = self.page.screenshot()
        img = Image.open(io.BytesIO(shot)).convert("RGB")
        x, y = self.x, self.y
        if self.crop:
            img = img.crop(self.crop)
            x, y = x - self.crop[0], y - self.crop[1]
        if self.chrome:
            img = self.draw_chrome(img)
            y += BAR_H
        if self.pointer_visible:
            self.draw_pointer(img, x, y, pressed)
        if key:
            self.draw_key(img, key)
        self.frames.append((img, ms))

    # -- actions ----------------------------------------------------------
    def place(self, x: float, y: float) -> None:
        self.x, self.y = x, y
        self.page.mouse.move(x, y)

    def move_to(self, x: float, y: float, duration_ms: int = 800) -> None:
        steps = max(2, duration_ms // FRAME_MS)
        x0, y0 = self.x, self.y
        for i in range(1, steps + 1):
            t = ease(i / steps)
            self.place(x0 + (x - x0) * t, y0 + (y - y0) * t)
            self.snap(FRAME_MS)

    def hold(self, ms: int, key: str | None = None) -> None:
        self.snap(ms, key=key)

    def click(self, after_ms: int = 0) -> None:
        self.snap(120, pressed=True)
        self.page.mouse.down()
        self.page.mouse.up()
        if after_ms:
            self.page.wait_for_timeout(after_ms)

    def save(self, path: Path) -> None:
        images = [f.quantize(colors=255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
                  for f, _ in self.frames]
        durations = [ms for _, ms in self.frames]
        path.parent.mkdir(parents=True, exist_ok=True)
        images[0].save(path, save_all=True, append_images=images[1:], duration=durations,
                       loop=0, optimize=True, disposal=1)
        print(f"{path.relative_to(REPO)}: {len(images)} frames, "
              f"{sum(durations) / 1000:.1f} s, {path.stat().st_size / 1e6:.2f} MB")


def wait_for_deck(page: Page) -> None:
    page.wait_for_function("window.Reveal && Reveal.isReady()")
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(800)


def new_page(browser, width: int, height: int) -> Page:
    context = browser.new_context(viewport={"width": width, "height": height})
    context.grant_permissions(["clipboard-read", "clipboard-write"])
    return context.new_page()


def record_open_slides(browser) -> None:
    page = new_page(browser, 1280, 720)
    page.goto(LOCAL_ROOT + "index.html")
    page.wait_for_load_state("networkidle")
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(500)

    rec = Recorder(page, chrome=True)
    button = page.get_by_role("link", name="View as presentation").bounding_box()
    bx, by = button["x"] + button["width"] * 0.55, button["y"] + button["height"] * 0.6

    rec.place(bx + 260, by + 230)
    rec.hold(1400)
    rec.move_to(bx, by, 900)
    rec.hold(500)
    rec.click()
    wait_for_deck(page)

    rec.pointer_visible = False
    rec.hold(2200)
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(600)
    rec.hold(700, key="→")
    rec.hold(2600)
    rec.save(OUT / "open-slides.gif")
    page.close()


def record_copy_code(browser) -> None:
    page = new_page(browser, 1600, 900)
    page.goto(LOCAL_ROOT + "slides/zalf-2026.html#/checkpoint-2")
    wait_for_deck(page)

    # Crop to the instruction and the code block: below the slide title and
    # short of the step list in the right-hand column.
    block = page.locator("section#checkpoint-2 div.sourceCode").first.bounding_box()
    intro = page.locator("section#checkpoint-2 .column p").first.bounding_box()
    crop = (
        int(max(0, intro["x"] - 28)),
        int(max(0, intro["y"] - 22)),
        int(min(1600, block["x"] + block["width"] + 14)),
        int(min(900, block["y"] + block["height"] + 28)),
    )
    rec = Recorder(page, chrome=False, crop=crop)

    # Start just below the block, so the copy button is hidden until the
    # pointer moves onto the code.
    rec.place(block["x"] + block["width"] * 0.8, block["y"] + block["height"] + 3)
    rec.hold(1200)
    rec.move_to(block["x"] + block["width"] * 0.62, block["y"] + block["height"] * 0.45, 800)
    rec.hold(700)
    copy = page.locator("section#checkpoint-2 .code-copy-button").first.bounding_box()
    rec.move_to(copy["x"] + copy["width"] * 0.45, copy["y"] + copy["height"] * 0.5, 700)
    rec.hold(400)
    rec.click(after_ms=100)
    # Step aside so the tick is visible, staying over the block: the icon
    # only shows while the mouse is over the code.
    rec.move_to(copy["x"] - 60, copy["y"] + 70, 150)
    rec.hold(2400)
    rec.save(OUT / "copy-code.gif")
    page.close()


def main() -> None:
    if not (SITE / "slides" / "zalf-2026.html").exists():
        raise SystemExit("Render the site first: _site/slides/zalf-2026.html is missing.")
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge")
        record_open_slides(browser)
        record_copy_code(browser)
        browser.close()


if __name__ == "__main__":
    main()

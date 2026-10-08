"""Turn a deck into pictures so every slide can be looked at before it is delivered.

Usage: preview.py <deck.pptx> <out_folder> [--dpi 80]

Writes one picture per slide (slide-01.png, slide-02.png, ...) and contact sheets of nine slides
(sheet-1.png, sheet-2.png, ...). Look at the sheets first, then open any single slide that needs a closer look.

Needs LibreOffice (soffice), pdftoppm (poppler-utils) and Pillow. If the Inter font is not installed,
the copies kept in ../fonts are installed for the current user first; without Inter the pictures are wrong.
"""
import glob
import os
import shutil
import subprocess
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))


def ensure_inter():
    listed = subprocess.run(["fc-list"], capture_output=True, text=True).stdout
    if "Inter-Regular" in listed or "Inter:style=Regular" in listed:
        return
    target = os.path.expanduser("~/.fonts")
    os.makedirs(target, exist_ok=True)
    for name in ("Inter-Regular.otf", "Inter-Bold.otf"):
        shutil.copy(os.path.join(HERE, "..", "fonts", name), target)
    subprocess.run(["fc-cache", "-f"], check=False)


def main():
    args = sys.argv[1:]
    dpi = args[args.index("--dpi") + 1] if "--dpi" in args else "80"
    deck, out = os.path.abspath(args[0]), os.path.abspath(args[1])
    os.makedirs(out, exist_ok=True)
    for old in glob.glob(os.path.join(out, "slide-*.png")) + glob.glob(os.path.join(out, "sheet-*.png")):
        os.remove(old)
    ensure_inter()
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", out, deck], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600)
    pdf = os.path.join(out, os.path.splitext(os.path.basename(deck))[0] + ".pdf")
    subprocess.run(["pdftoppm", "-png", "-r", dpi, pdf, os.path.join(out, "slide")], check=True)
    slides = sorted(glob.glob(os.path.join(out, "slide-*.png")))
    thumbs = [Image.open(f).convert("RGB").resize((660, 371)) for f in slides]
    for part in range(0, len(thumbs), 9):
        chunk = thumbs[part:part + 9]
        rows = (len(chunk) + 2) // 3
        sheet = Image.new("RGB", (3 * 660 + 12, rows * 371 + (rows - 1) * 6), (60, 60, 60))
        for i, im in enumerate(chunk):
            sheet.paste(im, ((i % 3) * 666, (i // 3) * 377))
        sheet.save(os.path.join(out, f"sheet-{part // 9 + 1}.png"))
    print(f"{len(slides)} slides -> {out}  (contact sheets: {(len(slides) + 8) // 9})")


if __name__ == "__main__":
    main()

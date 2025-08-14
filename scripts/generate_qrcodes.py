#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer

# === Config ===
BASE_URL    = "https://intralog-contact-card.netlify.app/?person="
VCARDS_DIR  = "vcards"
OUT_DIR     = "qrcodes-logo"
ASSETS_DIR  = "assets/photos"

MODULE      = "#2b2b2b"
EYE         = "#0693e3"
EYE_SIZE    = 7
BOX_PIX     = 10
BORDER_BOX  = 4

LOGO_FILE   = "logo.png"
LOGO_SCALE  = 0.25   # percent of QR width

# Ensure output folder
os.makedirs(OUT_DIR, exist_ok=True)

# Precompute MODULE RGB tuple
rgb_mod = tuple(int(MODULE.lstrip('#')[i:i+2], 16) for i in (0,2,4))

for fname in os.listdir(VCARDS_DIR):
    if not fname.lower().endswith(".vcf"):
        continue
    person = os.path.splitext(fname)[0]
    url    = BASE_URL + person

    # 1) Build QR
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=BOX_PIX,
        border=BORDER_BOX
    )
    qr.add_data(url)
    qr.make(fit=True)

    # 2) Render round modules
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=CircleModuleDrawer(),
        fill_color=MODULE,
        back_color="white"
    ).convert("RGB")

    w, h     = img.size
    modules  = qr.modules_count
    px       = BOX_PIX
    bpx      = BORDER_BOX * px
    esz      = EYE_SIZE * px

    # 3) Draw stylized eyes
    draw = ImageDraw.Draw(img)
    coords = [
        (bpx, bpx),
        ((bpx + (modules - EYE_SIZE)*px), bpx),
        (bpx, (bpx + (modules - EYE_SIZE)*px)),
    ]
    for x,y in coords:
        # outer
        draw.rectangle([(x,y),(x+esz,y+esz)], fill=EYE)
        # inset white
        inset = px
        draw.rectangle(
            [(x+inset,y+inset),(x+esz-inset,y+esz-inset)],
            fill="white"
        )
        # core
        core = 3*px
        cx = x + (esz-core)//2
        cy = y + (esz-core)//2
        draw.rectangle([(cx,cy),(cx+core,cy+core)], fill=EYE)

    # 4) Recolor any remaining black dots to MODULE gray
    pixels = img.load()
    for yy in range(h):
        for xx in range(w):
            if pixels[xx,yy] == (0,0,0):
                pixels[xx,yy] = rgb_mod

        # 5) Clear a pad-around square + paste logo
    logo = Image.open(os.path.join(ASSETS_DIR, LOGO_FILE)).convert("RGBA")
    logo_size = int(w * LOGO_SCALE)
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
    lx = (w - logo_size) // 2
    ly = (h - logo_size) // 2

    # pad in modules
    MODULE_PAD = 1    # how many modules of white clearance
    pad = MODULE_PAD * BOX_PIX

    # draw white rounded rect under logo
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [(lx - pad, ly - pad),
         (lx + logo_size + pad, ly + logo_size + pad)],
        radius=pad,       # roundness = pad
        fill="white"
    )

    # now paste the logo itself
    img.paste(logo, (lx, ly), logo)

    # 6) Save
    out = os.path.join(OUT_DIR, f"{person}.png")
    img.save(out)
    print("✅", out)

print("🎉 Done with logo‐integrated QRs!")

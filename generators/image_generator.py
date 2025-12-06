from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import uuid

# ensure static/tmp exists
os.makedirs(os.path.join("static", "tmp"), exist_ok=True)

# Try to pick a default font path. If on Debian/Render, DejaVu should exist.
DEFAULT_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def _load_font(size=120):
    try:
        return ImageFont.truetype(DEFAULT_FONT, size=size)
    except Exception:
        return ImageFont.load_default()

def make_cover_image(prompt_text: str, size: int = 1024, logo_path: str | None = None) -> str:
    """
    Make a square branded cover image with electric blue background and large white "XCELLRATE" text,
    plus the prompt_text as subheading. Optionally embed a small logo image if provided.
    Returns path to PNG file.
    """
    # Colors
    blue = (6, 82, 255)  # electric blue
    white = (255, 255, 255)
    accent = (0, 0, 0)

    img = Image.new("RGBA", (size, size), blue)
    draw = ImageDraw.Draw(img)

    # big title
    title_font = _load_font(int(size * 0.12))
    subtitle_font = _load_font(int(size * 0.05))

    title_text = "XCELLRATE"
    w, h = draw.textsize(title_text, font=title_font)
    draw.text(((size - w) / 2, size * 0.18), title_text, font=title_font, fill=white)

    # prompt text as subtitle (wrap)
    max_width = int(size * 0.8)
    lines = []
    words = prompt_text.split()
    cur = ""
    for word in words:
        test = cur + " " + word if cur else word
        tw, th = draw.textsize(test, font=subtitle_font)
        if tw > max_width:
            lines.append(cur)
            cur = word
        else:
            cur = test
    if cur:
        lines.append(cur)

    y = int(size * 0.36)
    for line in lines[:4]:
        tw, th = draw.textsize(line, font=subtitle_font)
        draw.text(((size - tw) / 2, y), line, font=subtitle_font, fill=white)
        y += int(th * 1.4)

    # small footer CTA
    cta_font = _load_font(int(size * 0.034))
    cta = "Get templates — link in bio"
    tw, th = draw.textsize(cta, font=cta_font)
    draw.text(((size - tw) / 2, size * 0.82), cta, font=cta_font, fill=white)

    # embed logo if provided (scale to 10% width)
    if logo_path and os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path).convert("RGBA")
            # scale
            w0, h0 = logo.size
            target_w = int(size * 0.12)
            scale = target_w / w0
            logo = logo.resize((int(w0 * scale), int(h0 * scale)), Image.LANCZOS)
            # paste top-right with some margin
            img.paste(logo, (size - logo.width - 30, 30), logo)
        except Exception:
            pass

    # subtle grain overlay
    try:
        overlay = Image.effect_noise((size, size), 20).convert("L")
        overlay = overlay.point(lambda p: p * 0.06)
        overlay = overlay.convert("RGBA")
        img = Image.alpha_composite(img, overlay)
    except Exception:
        pass

    out_name = f"static/tmp/cover_{uuid.uuid4().hex}.png"
    os.makedirs(os.path.dirname(out_name), exist_ok=True)
    img.convert("RGB").save(out_name, "PNG", quality=90)
    return out_name

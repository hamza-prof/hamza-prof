"""
Inject assets/me.svg (a 1344x768 vector portrait trace) into the portrait
panel of assets/header-terminal.svg.

GitHub renders SVGs via <img>, which blocks external references — so the
portrait MUST be inlined. This script does that between the START_AVATAAR /
END_AVATAR markers in the header template, idempotently.

me.svg is landscape (1.75:1); the panel is 220x170 (1.29:1). We scale to
"cover" the panel (fit height, overflow clipped by portraitClip) and
horizontally center the source. Tweak scale / translate_x / translate_y
below to reframe the face if needed.
"""
import os
import re

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
ME_SVG = os.path.join(ASSETS, "me.svg")
HEADER_SVG = os.path.join(ASSETS, "header-terminal.svg")

# Panel geometry (must match header-terminal.svg's portraitClip rect)
PANEL_X, PANEL_Y = 24, 54
PANEL_W, PANEL_H = 220, 170

# Source geometry (me.svg)
SRC_W, SRC_H = 1344, 768

# "Cover" scale: use the larger of (panel_w/src_w, panel_h/src_h) so the panel
# is fully filled. src is wider than tall relative to panel, so height wins.
cover = max(PANEL_W / SRC_W, PANEL_H / SRC_H)   # = 170/768 ≈ 0.2214
scale = cover

scaled_w = SRC_W * scale                         # ≈ 297.5 (overflows panel width)
# Center horizontally inside the panel; top-align vertically (face sits high).
translate_x = PANEL_X + (PANEL_W - scaled_w) / 2  # ≈ -14.75
translate_y = PANEL_Y                              # top-align

# Allow easy manual overrides:
# scale = 0.25
# translate_x = -40
# translate_y = 40


def main():
    if not os.path.exists(ME_SVG):
        print(f"Error: {ME_SVG} not found.")
        return
    if not os.path.exists(HEADER_SVG):
        print(f"Error: {HEADER_SVG} not found.")
        return

    with open(ME_SVG, "r", encoding="utf-8") as f:
        me_content = f.read()

    body = re.search(r"<svg[^>]*>(.*)</svg>", me_content, re.DOTALL)
    me_data = body.group(1).strip() if body else me_content

    avatar_block = f"""    <!-- START_AVATAR -->
    <g transform="translate({translate_x}, {translate_y}) scale({scale})">
      {me_data}
    </g>
    <!-- END_AVATAR -->"""

    with open(HEADER_SVG, "r", encoding="utf-8") as f:
        content = f.read()

    if "<!-- START_AVATAR -->" in content and "<!-- END_AVATAR -->" in content:
        content = re.sub(
            r"<!-- START_AVATAR -->.*?<!-- END_AVATAR -->",
            lambda m: avatar_block,
            content,
            flags=re.DOTALL,
        )
    else:
        # Fallback: inject right before the scan-line comment
        content = content.replace(
            "    <!-- Scan line sweeping over the portrait -->",
            f"{avatar_block}\n    <!-- Scan line sweeping over the portrait -->",
        )

    # Collapse accidental double blanks
    content = re.sub(r"\n\s*\n\s*\n", "\n\n", content)

    with open(HEADER_SVG, "w", encoding="utf-8") as f:
        f.write(content)

    print(
        f"Injected me.svg into header-terminal.svg "
        f"(scale={scale:.5f}, tx={translate_x:.2f}, ty={translate_y:.2f})."
    )


if __name__ == "__main__":
    main()
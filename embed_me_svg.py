import os
import re

def embed_svg():
    base_path = r"\\wsl.localhost\Ubuntu-22.04\home\hamza\hamza-prof\assets"
    full_svg_path = os.path.join(base_path, "full.svg")
    terminal_svg_path = os.path.join(base_path, "terminal-intro.svg")

    if not os.path.exists(full_svg_path):
        print(f"Error: {full_svg_path} not found.")
        return

    with open(full_svg_path, 'r', encoding='utf-8') as f:
        avatar_content = f.read()

    avatar_body = re.search(r'<svg[^>]*>(.*)</svg>', avatar_content, re.DOTALL)
    if avatar_body:
        avatar_data = avatar_body.group(1).strip()
    else:
        avatar_data = avatar_content

    # Target Dimensions
    # Terminal: 850 x 480
    # Desired: Standing on floor. Top padding 15.
    # Height: 480 - 15 = 465.
    # Original Height: 768.
    # Scale = 465 / 768 = 0.60546875
    scale = 0.60546875
    
    # X Position Adjustment for "Right Side"
    # Source SVG width: 1344. Character is roughly centered at ~672.
    # Scaled center is ~406. 
    # Scaled Width is ~813. 
    # To place the character on the far right (say, centered at X=700 in terminal),
    # we need translate_x = 700 - 406 = 294.
    
    translate_x = 280.0
    translate_y = 15.0
    
    # Shadow position: should follow the character's horizontal center
    # Character center in original is ~672. 
    # Actual Shadow X = translate_x + (672 * scale) = 280 + 406.8 = 686.8.
    shadow_x = 686.8

    spotlight_def = """
    <defs id="avatarDefs">
        <radialGradient id="floorSpotlight" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
            <stop offset="0%" style="stop-color:#ffffff;stop-opacity:0.1" />
            <stop offset="100%" style="stop-color:#ffffff;stop-opacity:0" />
        </radialGradient>
    </defs>
    """
    
    shadow_element = f"""
    <g transform="translate({shadow_x}, 470)">
        <ellipse cx="0" cy="0" rx="80" ry="8" fill="#000000" opacity="0.4">
            <animate attributeName="rx" values="80;90;80" dur="4s" repeatCount="indefinite" />
            <animate attributeName="opacity" values="0.4;0.2;0.4" dur="4s" repeatCount="indefinite" />
        </ellipse>
        <ellipse cx="0" cy="0" rx="160" ry="30" fill="url(#floorSpotlight)" opacity="0.6" />
    </g>
    """

    # Wrapped Content with markers
    new_avatar_block = f"""
    <!-- START_AVATAR -->
    <g id="creativeAvatar">
        {spotlight_def}
        {shadow_element}
        <g transform="translate({translate_x}, {translate_y}) scale({scale})">
            {avatar_data}
        </g>
    </g>
    <!-- END_AVATAR -->
    """

    with open(terminal_svg_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # AGGRESSIVE CLEANING
    # 1. Clean anything between markers
    content = re.sub(r'<!-- START_AVATAR -->.*?<!-- END_AVATAR -->', '', content, flags=re.DOTALL)
    
    # 2. Clean previous "Creative Avatar Group" manually
    content = re.sub(r'<!-- Creative Avatar Group \(Standing\) -->.*?<g transform="translate\([0-9\.]+, [0-9\.]+\) scale\([0-9\.]+\)">.*?</g>', '', content, flags=re.DOTALL)
    
    # 3. Clean any stray groups from previous failures that might still be there 
    # (specifically the one with scale 0.6054... occurring multiple times)
    content = re.sub(r'<g transform="translate\([0-9\.]+, [0-9\.]+\) scale\(0\.60546875\)">.*?</g>', '', content, flags=re.DOTALL)

    # 4. Clean any definitions that might have been duplicated
    content = re.sub(r'<defs id="avatarDefs">.*?</defs>', '', content, flags=re.DOTALL)
    content = re.sub(r'<!-- Window Controls -->', '<!-- Window Controls -->', content) # No-op just to be safe

    # Clean up empty lines
    content = re.sub(r'\n\s*\n', '\n', content)

    # INSERTION
    if '</svg>' in content:
        final_content = content.replace('</svg>', f'\n{new_avatar_block}\n</svg>')
    else:
        final_content = content + f'\n{new_avatar_block}\n</svg>'

    # Write back
    with open(terminal_svg_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"Successfully re-embedded full.svg at X={translate_x} (Right Side).")

if __name__ == "__main__":
    embed_svg()

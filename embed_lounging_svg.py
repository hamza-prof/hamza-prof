import os
import re

def embed_lounging_character():
    base_path = r"\\wsl.localhost\Ubuntu-22.04\home\hamza\hamza-prof\assets"
    lying_svg_path = os.path.join(base_path, "lying.svg")
    terminal_svg_path = os.path.join(base_path, "terminal-experience.svg")

    if not os.path.exists(lying_svg_path):
        print(f"Error: {lying_svg_path} not found.")
        return

    # Read lying character data
    with open(lying_svg_path, 'r', encoding='utf-8') as f:
        lying_content = f.read()

    lying_body = re.search(r'<svg[^>]*>(.*)</svg>', lying_content, re.DOTALL)
    lying_data = lying_body.group(1).strip() if lying_body else lying_content

    # Target: Lounging at the bottom of the terminal.
    # Terminal background ends at Y=1080.
    # We want NO GAP. 
    # Based on the user's feedback image, the previous Y=800 left a huge gap.
    # The paths in lying.svg have large internal offsets.
    # Let's push it down significantly. Y=920 or more.
    scale = 0.45
    translate_x = -20 # Shift left a bit more to really "lie" inside the window
    translate_y = 960 # Pushing down aggressively to hit the floor

    lounging_character = f"""
    <!-- START_LOUNGING_CHARACTER -->
    <g id="loungingGroup" transform="translate({translate_x}, {translate_y}) scale({scale})">
        <!-- Re-grounded Floor Shadow -->
        <ellipse cx="600" cy="580" rx="600" ry="30" fill="#000000" opacity="0.4" filter="blur(10px)"/>
        {lying_data}
    </g>
    <!-- END_LOUNGING_CHARACTER -->
    """

    with open(terminal_svg_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Maintain height at 1250 to allow for the dangling leg below the floor
    content = re.sub(r'height="[0-9]+"', 'height="1250"', content, count=1)
    content = re.sub(r'viewBox="0 0 850 [0-9]+"', 'viewBox="0 0 850 1250"', content, count=1)
    
    # Ensure terminal rect is fixed at 1080 (floor)
    content = re.sub(r'<rect x="0" y="0" width="830" height="[0-9]+" rx="12" fill="url\(#termBg\)"/>', '<rect x="0" y="0" width="830" height="1080" rx="12" fill="url(#termBg)"/>', content)
    # Ensure shadow is fixed too
    content = re.sub(r'<rect x="10" y="10" width="830" height="[0-9]+" rx="12" fill="#000000" opacity="0.3"/>', '<rect x="10" y="10" width="830" height="1080" rx="12" fill="#000000" opacity="0.3"/>', content)

    # Cleaning previous markers
    content = re.sub(r'<!-- START_LOUNGING_CHARACTER -->.*?<!-- END_LOUNGING_CHARACTER -->', '', content, flags=re.DOTALL)

    # Insertion before closing svg
    if '</svg>' in content:
        final_content = content.replace('</svg>', f'\n{lounging_character}\n</svg>')
    else:
        final_content = content + f'\n{lounging_character}\n</svg>'

    # Clean up excessive whitespace
    final_content = re.sub(r'\n\s*\n', '\n', final_content)

    with open(terminal_svg_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print("Successfully grounded lounging character (removed cup) in terminal-experience.svg.")

if __name__ == "__main__":
    embed_lounging_character()

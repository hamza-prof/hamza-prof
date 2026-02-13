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

    scale = 0.45
    translate_x = -20 
    translate_y = 960 

    # LOOPER CSS + SVG Structure
    # 12s total loop: 4s per phrase
    # JetBrains Mono/Consolas 15px typical width is 9px per char.
    # P1 (31 chars): 279px
    # P2 (29 chars): 261px
    # P3 (27 chars): 243px

    lounging_character = f"""
    <!-- START_LOUNGING_CHARACTER -->
    <style>
      .quote-item {{ opacity: 0; }}
      .cursor-item {{ opacity: 0; }}
      
      /* Phase Transitions (12s total) */
      .p1 {{ animation: cycleP1 12s step-end infinite; }}
      .p2 {{ animation: cycleP2 12s step-end infinite; }}
      .p3 {{ animation: cycleP3 12s step-end infinite; }}
      
      @keyframes cycleP1 {{ 0%, 33.32% {{ opacity: 1; }} 33.33%, 100% {{ opacity: 0; }} }}
      @keyframes cycleP2 {{ 0%, 33.32% {{ opacity: 0; }} 33.33%, 66.65% {{ opacity: 1; }} 66.66%, 100% {{ opacity: 0; }} }}
      @keyframes cycleP3 {{ 0%, 66.65% {{ opacity: 0; }} 66.66%, 99.99% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}

      /* Typing Animations */
      #maskRect1 {{ animation: typeP1 12s steps(31) infinite; }}
      #maskRect2 {{ animation: typeP2 12s steps(29) infinite; }}
      #maskRect3 {{ animation: typeP3 12s steps(27) infinite; }}

      @keyframes typeP1 {{
        0% {{ width: 0; }}
        20%, 30% {{ width: 279px; }}
        33.33%, 100% {{ width: 0; }}
      }}
      @keyframes typeP2 {{
        0%, 33.33% {{ width: 0; }}
        53.33%, 63.33% {{ width: 261px; }}
        66.66%, 100% {{ width: 0; }}
      }}
      @keyframes typeP3 {{
        0%, 66.66% {{ width: 0; }}
        86.66%, 96.66% {{ width: 243px; }}
        100% {{ width: 0; }}
      }}

      /* Cursor Movements */
      #cursorItem1 {{ animation: moveC1 12s steps(31) infinite, blink 1s step-end infinite; }}
      #cursorItem2 {{ animation: moveC2 12s steps(29) infinite, blink 1s step-end infinite; }}
      #cursorItem3 {{ animation: moveC3 12s steps(27) infinite, blink 1s step-end infinite; }}

      @keyframes moveC1 {{
        0% {{ x: 0; opacity: 1; }}
        20%, 30% {{ x: 279px; opacity: 1; }}
        33.33%, 100% {{ x: 0; opacity: 0; }}
      }}
      @keyframes moveC2 {{
        0%, 33.33% {{ x: 0; opacity: 0; }}
        33.34% {{ x: 0; opacity: 1; }}
        53.33%, 63.33% {{ x: 261px; opacity: 1; }}
        66.66%, 100% {{ x: 0; opacity: 0; }}
      }}
      @keyframes moveC3 {{
        0%, 66.66% {{ x: 0; opacity: 0; }}
        66.67% {{ x: 0; opacity: 1; }}
        86.66%, 96.66% {{ x: 243px; opacity: 1; }}
        100% {{ x: 0; opacity: 0; }}
      }}
    </style>

    <g id="loungingGroup" transform="translate({translate_x}, {translate_y}) scale({scale})">
        <!-- Floor Shadow -->
        <ellipse cx="600" cy="580" rx="600" ry="30" fill="#000000" opacity="0.4" filter="blur(10px)"/>
        {lying_data}
    </g>
    
    <!-- Looping Typewriter Quote -->
    <g transform="translate(60, 1050)">
        <defs>
            <clipPath id="mask1"><rect id="maskRect1" x="0" y="-15" width="0" height="30" /></clipPath>
            <clipPath id="mask2"><rect id="maskRect2" x="0" y="-15" width="0" height="30" /></clipPath>
            <clipPath id="mask3"><rect id="maskRect3" x="0" y="-15" width="0" height="30" /></clipPath>
        </defs>
        
        <!-- Phrase 1 -->
        <g class="quote-item p1" clip-path="url(#mask1)">
            <text class="cmd-text" font-size="15px" fill="#7aa2f7">
                ❯ status: <tspan fill="#bb9af7">innovating_at_rest</tspan>...
            </text>
        </g>
        <rect id="cursorItem1" class="cursor-item p1" x="0" y="-14" width="8" height="18" fill="#a78bfa" />

        <!-- Phrase 2 -->
        <g class="quote-item p2" clip-path="url(#mask2)">
            <text class="cmd-text" font-size="15px" fill="#7aa2f7">
                ❯ status: <tspan fill="#79bbff">dreaming_in_code</tspan>...
            </text>
        </g>
        <rect id="cursorItem2" class="cursor-item p2" x="0" y="-14" width="8" height="18" fill="#a78bfa" />

        <!-- Phrase 3 -->
        <g class="quote-item p3" clip-path="url(#mask3)">
            <text class="cmd-text" font-size="15px" fill="#7aa2f7">
                ❯ status: <tspan fill="#9ece6a">scaling_dreams</tspan>...
            </text>
        </g>
        <rect id="cursorItem3" class="cursor-item p3" x="0" y="-14" width="8" height="18" fill="#a78bfa" />
    </g>
    <!-- END_LOUNGING_CHARACTER -->
    """

    with open(terminal_svg_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Insertion logic
    content = re.sub(r'<!-- START_LOUNGING_CHARACTER -->.*?<!-- END_LOUNGING_CHARACTER -->', '', content, flags=re.DOTALL)
    if '</svg>' in content:
        final_content = content.replace('</svg>', f'\n{lounging_character}\n</svg>')
    else:
        final_content = content + f'\n{lounging_character}\n</svg>'

    # Clean up whitespace
    final_content = re.sub(r'\n\s*\n', '\n', final_content)

    with open(terminal_svg_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print("Successfully implemented precise looping cursor in terminal-experience.svg.")

if __name__ == "__main__":
    embed_lounging_character()

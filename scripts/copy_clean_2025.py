import os

# Read clean_2025_md.md if available
if os.path.exists('clean_2025_md.md'):
    with open('clean_2025_md.md', 'r', encoding='utf-8') as f:
        md_data = f.read()
    with open('clean_2025_urls.txt', 'r', encoding='utf-8') as f:
        txt_data = f.read()

    target_md = os.path.abspath('Sensebar_AI_Agent_Videos_Full_Version.md')
    target_txt = os.path.abspath('sensebar_urls_for_notebooklm.txt')

    with open(target_md, 'w', encoding='utf-8') as f:
        f.write(md_data)

    with open(target_txt, 'w', encoding='utf-8') as f:
        f.write(txt_data)

    print("SUCCESSFULLY OVERWROTE SENSEBAR FILES WITH CLEAN 2025-2026 DATA!")
else:
    print("clean_2025_md.md not found in", os.getcwd())

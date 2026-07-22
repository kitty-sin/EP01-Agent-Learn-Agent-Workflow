import os
import shutil

src_md = 'Sensebar_AI_Agent_Videos_Full_Version.md'
src_txt = 'sensebar_urls_for_notebooklm.txt'

with open(src_md, 'r', encoding='utf-8') as f:
    content_md = f.read()

with open(src_txt, 'r', encoding='utf-8') as f:
    content_txt = f.read()

paths = [
    r"C:\Users\PC\Documents\Google%20Antigravity\2026-AI-Agent\Al_AgentEP01_用Agent來學習Agent",
    r"C:\Users\PC\Documents\Google Antigravity\2026-AI-Agent\Al_AgentEP01_用Agent來學習Agent"
]

for p in paths:
    os.makedirs(p, exist_ok=True)
    f_md = os.path.join(p, 'Sensebar_AI_Agent_Videos_Full_Version.md')
    f_txt = os.path.join(p, 'sensebar_urls_for_notebooklm.txt')
    with open(f_md, 'w', encoding='utf-8') as f:
        f.write(content_md)
    with open(f_txt, 'w', encoding='utf-8') as f:
        f.write(content_txt)
    print("Wrote to path:", p)

print("FORCE COPY ALL PATHS COMPLETED!")

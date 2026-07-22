import os
import shutil

src_md = 'Sensebar_AI_Agent_Videos_Full_Version.md'
src_txt = 'sensebar_urls_for_notebooklm.txt'

target_dir_decoded = r"C:\Users\PC\Documents\Google Antigravity\2026-AI-Agent\Al_AgentEP01_用Agent來學習Agent"

if os.path.exists(target_dir_decoded):
    dst_md = os.path.join(target_dir_decoded, 'Sensebar_AI_Agent_Videos_Full_Version.md')
    dst_txt = os.path.join(target_dir_decoded, 'sensebar_urls_for_notebooklm.txt')
    shutil.copyfile(src_md, dst_md)
    shutil.copyfile(src_txt, dst_txt)
    print("Successfully copied to decoded path:", target_dir_decoded)
else:
    print("Decoded path does not exist, skipping copy.")

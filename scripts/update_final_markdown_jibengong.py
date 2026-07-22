import re
import os
import subprocess

cn_digits = {
    '一': '01', '二': '02', '三': '03', '四': '04', '五': '05',
    '六': '06', '七': '07', '八': '08', '九': '09', '十': '10'
}

def clean_jibengong_line(line):
    # Skip header quotes starting with >
    if line.strip().startswith('>'):
        return line

    # EXCEPTION: Do not modify "Claude基本功EP09_1 : 5 分鐘學會！Claude 串接 Firebase 資料庫全攻略懶人包。"
    if "Claude基本功EP09_1" in line or "EBwFeyTvcR8" in line:
        return line

    if "基本功" not in line:
        return line

    # Only format lines that start with an item number e.g. "1. " or "25. "
    m_num = re.match(r'^(\d+\.\s+)?(.*)$', line)
    if not m_num or not m_num.group(1):
        return line

    item_prefix = m_num.group(1)
    content = m_num.group(2).strip()

    pos = content.find("基本功")
    if pos == -1:
        return line

    raw_xx = content[:pos].strip()
    remainder = content[pos + len("基本功"):].strip()

    xx_clean = re.sub(r'[^\w]', '', raw_xx.lower())
    if "claudecode" in xx_clean:
        xx = "Claude Code"
    elif "claude" in xx_clean:
        xx = "Claude"
    elif "gptcodex" in xx_clean or "codex" in xx_clean:
        xx = "GPT Codex"
    elif "opencode" in xx_clean or "open" in xx_clean:
        xx = "OpenCode"
    elif "antigravity" in xx_clean or "anti" in xx_clean:
        xx = "AntiGravity"
    elif "chatgptapp" in xx_clean or "chatgpt" in xx_clean:
        xx = "ChatGPT App"
    elif "googleai" in xx_clean or "google" in xx_clean:
        xx = "Google AI"
    elif "aiagent" in xx_clean or "agent" in xx_clean:
        xx = "AI Agent"
    else:
        xx = raw_xx if raw_xx else "AI Agent"

    ep_num = ""
    rest_desc = remainder

    m_cn = re.search(r'^(?:第)?([一二三四五六七八九十]|\d{1,2})\s*[:：,_,\s]*(.*)$', remainder)
    if m_cn and m_cn.group(1) in cn_digits:
        ep_num = cn_digits[m_cn.group(1)]
        rest_desc = m_cn.group(2)
    else:
        m_ep = re.search(r'^(?:[:：\s]*EP\s*|ep\s*|_EP\s*|_ep\s*)?(\d{1,2}(?:\s+\d{1,2})?)\s*[:：,_,\s]*(.*)$', remainder, re.IGNORECASE)
        if m_ep:
            raw_ep = m_ep.group(1).replace(" ", "")
            if len(raw_ep) == 1:
                ep_num = f"0{raw_ep}"
            else:
                ep_num = raw_ep
            rest_desc = m_ep.group(2)
        else:
            ep_num = "01"
            rest_desc = remainder

    rest_desc = re.sub(r'^[：:\s,_]+', '', rest_desc).strip()

    # Format as requested: "XX 基本功 EP** : Description"
    new_line = f"{item_prefix}{xx} 基本功 EP{ep_num} : {rest_desc}"
    return new_line

# Reset cleanly
subprocess.run(['python', 'build_perfect_utf8_markdown.py'])

with open('Sensebar_AI_Agent_Videos_Full_Version.md', 'r', encoding='utf-8') as f:
    raw_text = f.read()

lines = raw_text.splitlines()
new_lines = [clean_jibengong_line(l) for l in lines]
new_text = "\n".join(new_lines)

paths = [
    r'c:\Users\PC\Documents\Google%20Antigravity\2026-AI-Agent\Al_AgentEP01_用Agent來學習Agent',
    r'C:\Users\PC\Documents\Google Antigravity\2026-AI-Agent\Al_AgentEP01_用Agent來學習Agent',
    os.getcwd()
]

for p in paths:
    try:
        os.makedirs(p, exist_ok=True)
        with open(os.path.join(p, 'Sensebar_AI_Agent_Videos_Full_Version.md'), 'w', encoding='utf-8') as f:
            f.write(new_text)
    except Exception as e:
        print("Err:", e)

print("SUCCESSFULLY RE-APPLIED UNIFIED 基本功 FORMATTING TO ALL PATHS!")

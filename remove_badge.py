import re
import glob

html_files = glob.glob("*.html")
for file in html_files:
    with open(file, "r", encoding="utf-8") as f:
        c = f.read()
    c = re.sub(r'<span style="background: rgba\(0, 210, 106, 0\.1\); border: 1px solid var\(--primary-600\); padding: 2px 8px; border-radius: 4px; font-weight: 800; color: var\(--primary-600\); font-size: 0\.75rem;">GOV\.UZ</span>', '', c)
    with open(file, "w", encoding="utf-8") as f:
        f.write(c)
print("Removed GOV.UZ badge from all headers.")

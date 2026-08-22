import re

with open("css/styles.css", "r", encoding="utf-8") as f:
    content = f.read()

# Fix form-input focus shadow
content = content.replace("rgba(16, 185, 129, 0.1)", "rgba(0, 210, 106, 0.15)")

# Remove footer links hover translation
content = content.replace("transform: translateX(4px);", "")

with open("css/styles.css", "w", encoding="utf-8") as f:
    f.write(content)

print("styles.css minor tech tweaks applied")

import re

with open("css/styles.css", "r", encoding="utf-8") as f:
    content = f.read()

# Replace border radii
content = content.replace("var(--radius-xl)", "var(--radius-md)")
content = content.replace("var(--radius-lg)", "var(--radius-md)")
content = content.replace("var(--radius-full)", "var(--radius-md)")
# EXCEPT for rounded images, wait. If they are avatars we might want them rounded, but high-tech often uses square avatars or slightly rounded. radius-md is 2px now.

# Remove bouncy translations and rotations
content = re.sub(r'transform:\s*translateY\(-[0-9]+px\);', '', content)
content = re.sub(r'transform:\s*translateY\(-[0-9]+px\)\s*scale\([0-9\.]+\);', '', content)
content = re.sub(r'transform:\s*scale\([0-9\.]+\)\s*rotate\([0-9\-]+deg\);', 'transform: scale(1.05);', content)

with open("css/styles.css", "w", encoding="utf-8") as f:
    f.write(content)

print("styles.css cleaned of bouncy animations and overly rounded corners.")

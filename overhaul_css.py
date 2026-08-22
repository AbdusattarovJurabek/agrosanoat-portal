import re

with open("css/styles.css", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the font import
content = content.replace("family=Outfit:wght@400;500;600;700;800;900", "family=Montserrat:wght@400;500;600;700;800;900")
content = content.replace("'Outfit'", "'Montserrat'")

# Rewrite root variables for High-Tech Dark Theme
new_root = """:root {
  /* High-Tech Premium Color Palette */
  --primary-900: #022c22;
  --primary-800: #064e3b;
  --primary-700: #00b057;
  --primary-600: #00d26a; /* Electric Emerald */
  --primary-500: #10b981;
  --primary-400: #34d399;
  --primary-100: #d1fae5;
  --primary-50: #ecfdf5;

  --accent-gold: #fbbf24;
  --accent-amber: #f59e0b;
  --accent-yellow: #fbbf24;
  --accent-light: #fef3c7;

  --slate-900: #0B0F19; /* Deep tech background */
  --slate-800: #111827; /* Cards */
  --slate-700: #1F2937;
  --slate-600: #374151;
  --slate-500: #4B5563;
  --slate-400: #9CA3AF;
  --slate-300: #D1D5DB;
  --slate-200: #E5E7EB;
  --slate-100: #F3F4F6;
  --slate-50: #F9FAFB;

  /* Theme Variables (Forced Dark Tech) */
  --bg-body: var(--slate-900);
  --bg-card: var(--slate-800);
  --bg-card-hover: var(--slate-700);
  --bg-header: rgba(11, 15, 25, 0.95);
  --bg-secondary: #0d1321;
  --bg-glass: rgba(17, 24, 39, 0.8);
  --bg-glass-heavy: rgba(17, 24, 39, 0.95);

  --text-main: #F9FAFB;
  --text-muted: #9CA3AF;
  --text-inverse: #0B0F19;

  --border-color: rgba(255, 255, 255, 0.1);
  --border-light: rgba(255, 255, 255, 0.15);
  --border-focus: var(--primary-600);

  /* Tech Shadows (Sharp) */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.5);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.5);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.7);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.8);
  --shadow-glow: 0 0 15px rgba(0, 210, 106, 0.3);
  --shadow-glow-amber: 0 0 15px rgba(245, 158, 11, 0.3);

  /* Sharp Tech Radii */
  --radius-sm: 0px;
  --radius-md: 2px;
  --radius-lg: 4px;
  --radius-xl: 6px;
  --radius-full: 4px; /* Remove bubbles */

  /* Typography */
  --font-main: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-heading: 'Montserrat', sans-serif;

  /* Sharp Transitions */
  --transition-fast: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
  --transition-normal: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  --transition-slow: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Force Dark Mode always for this UI */
[data-theme="dark"], [data-theme="light"] {
  /* It inherits from root, no overrides needed since root is dark */
}"""

content = re.sub(r':root\s*\{.*?\}(?=\s*/\* Dark Mode Overrides \*/)', new_root, content, flags=re.DOTALL)
content = re.sub(r'\[data-theme="dark"\]\s*\{.*?\}', '/* Dark Mode Overrides removed, using forced root */', content, flags=re.DOTALL)

with open("css/styles.css", "w", encoding="utf-8") as f:
    f.write(content)

print("styles.css updated to High-Tech Dark Theme")

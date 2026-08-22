import re

with open("css/styles.css", "r", encoding="utf-8") as f:
    content = f.read()

old_hero_css = """/* Hero Section */
.hero-section {
  position: relative;
  min-height: 85vh;
  display: flex;
  align-items: center;
  background: url('../assets/hero_agri.jpg') center/cover no-repeat;
  color: #ffffff;
  padding: 8rem 0 10rem;
  overflow: hidden;
}

.hero-overlay-grid {
  position: absolute;
  inset: 0;
  background: 
    linear-gradient(135deg, rgba(2, 44, 34, 0.95) 0%, rgba(15, 23, 42, 0.8) 100%),
    radial-gradient(circle at top right, rgba(16, 185, 129, 0.2), transparent 50%);
}

.hero-content {
  position: relative;
  z-index: 10;
  max-width: 850px;
  text-align: center;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--radius-full);
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--accent-light);
  margin-bottom: 2rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.hero-badge i { color: var(--accent-amber); }

.hero-title {
  font-size: clamp(2.5rem, 5vw, 4.5rem);
  font-weight: 900;
  line-height: 1.1;
  color: #ffffff;
  margin-bottom: 1.5rem;
  letter-spacing: -0.03em;
  text-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.hero-title span {
  background: linear-gradient(135deg, var(--accent-yellow) 0%, var(--accent-amber) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

.hero-description {
  font-size: clamp(1.1rem, 2vw, 1.35rem);
  color: rgba(255,255,255,0.85);
  margin-bottom: 3rem;
  line-height: 1.6;
  max-width: 700px;
  font-weight: 400;
}

.hero-cta-group {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.hero-search-box {
  margin-top: 3.5rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 0.5rem 0.5rem 0.5rem 1.5rem;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
  max-width: 680px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.2);
  transition: var(--transition-normal);
}

.hero-search-box:focus-within {
  background: rgba(255, 255, 255, 0.15);
  border-color: var(--primary-400);
  box-shadow: var(--shadow-glow);
}

.hero-search-box i { color: #cbd5e1; font-size: 1.2rem; }
.hero-search-box input {
  flex: 1;
  background: none;
  border: none;
  outline: none;
  color: #ffffff;
  font-size: 1.05rem;
  font-family: var(--font-main);
}
.hero-search-box input::placeholder { color: rgba(255,255,255,0.6); }"""

new_hero_css = """/* Hero Section */
.hero-section {
  position: relative;
  min-height: 90vh;
  display: flex;
  align-items: center;
  background: url('../assets/hero_agri.jpg') center/cover no-repeat;
  color: #ffffff;
  padding: 8rem 0 10rem;
  overflow: hidden;
  border-bottom: 1px solid var(--border-color);
}

.hero-overlay-grid {
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, rgba(11, 15, 25, 0.98) 0%, rgba(11, 15, 25, 0.8) 100%);
}

.hero-content {
  position: relative;
  z-index: 10;
  max-width: 900px;
  text-align: left;
  margin: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 1rem;
  background: rgba(0, 210, 106, 0.05);
  border: 1px solid var(--primary-600);
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--primary-600);
  margin-bottom: 2rem;
}

.hero-badge i { color: var(--primary-600); }

.hero-title {
  font-size: clamp(3rem, 6vw, 5rem);
  font-weight: 900;
  line-height: 1.05;
  color: #ffffff;
  margin-bottom: 1.5rem;
  letter-spacing: 0.02em;
  text-transform: uppercase;
}

.hero-title span {
  color: var(--primary-600);
}

.hero-description {
  font-size: clamp(1.1rem, 2vw, 1.25rem);
  color: var(--slate-300);
  margin-bottom: 3.5rem;
  line-height: 1.7;
  max-width: 700px;
  font-weight: 400;
}

.hero-cta-group {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.hero-search-box {
  margin-top: 4rem;
  background: rgba(11, 15, 25, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 0.5rem 0.5rem 0.5rem 1.5rem;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
  max-width: 680px;
  transition: var(--transition-fast);
}

.hero-search-box:focus-within {
  border-color: var(--primary-600);
  background: rgba(11, 15, 25, 0.9);
}

.hero-search-box i { color: var(--slate-400); font-size: 1.2rem; }
.hero-search-box input {
  flex: 1;
  background: none;
  border: none;
  outline: none;
  color: #ffffff;
  font-size: 1.05rem;
  font-family: var(--font-main);
}
.hero-search-box input::placeholder { color: var(--slate-500); }"""

if old_hero_css in content:
    content = content.replace(old_hero_css, new_hero_css)
    with open("css/styles.css", "w", encoding="utf-8") as f:
        f.write(content)
    print("styles.css hero section updated to Tech Theme")
else:
    print("Could not find exact hero section text to replace.")

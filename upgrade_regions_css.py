import re

with open("css/styles.css", "r", encoding="utf-8") as f:
    css_content = f.read()

new_region_css = """/* Regional Layout */
.regional-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: start;
}

.region-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.region-btn {
  padding: 1rem 1.5rem;
  background: var(--bg-secondary);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: var(--radius-sm);
  text-align: left;
  font-weight: 600;
  color: var(--slate-300);
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: var(--transition-fast);
}

.region-btn:hover, .region-btn.active {
  background: rgba(0, 210, 106, 0.1);
  border-color: var(--primary-600);
  color: var(--primary-600);
}

.region-detail-card {
  background: linear-gradient(180deg, var(--slate-800) 0%, rgba(17,24,39,0.4) 100%);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: var(--radius-md);
  padding: 2.5rem;
  position: sticky;
  top: 120px;
}
.region-detail-card h3 {
  font-size: 1.5rem;
  color: var(--text-main);
  margin-bottom: 1.5rem;
  text-transform: uppercase;
}
.detail-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
.detail-item:last-child {
  margin-bottom: 0; padding-bottom: 0; border-bottom: none;
}
.detail-icon {
  width: 40px;
  height: 40px;
  background: rgba(0, 210, 106, 0.1);
  color: var(--primary-600);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}
.detail-text h4 {
  font-size: 0.9rem;
  color: var(--slate-400);
  margin-bottom: 0.25rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.detail-text p {
  color: var(--text-main);
  font-weight: 500;
  font-size: 1.05rem;
}"""

css_content = re.sub(r'/\* Regional Layout \*/.*?(?=\/\* News Section \*\/)', new_region_css + "\n\n", css_content, flags=re.DOTALL)

with open("css/styles.css", "w", encoding="utf-8") as f:
    f.write(css_content)

print("Regions CSS upgraded.")

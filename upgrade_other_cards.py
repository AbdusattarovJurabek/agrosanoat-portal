import re

with open("css/styles.css", "r", encoding="utf-8") as f:
    css_content = f.read()

leader_css_new = """
.leader-card {
  background: linear-gradient(180deg, var(--slate-800) 0%, rgba(17,24,39,0.4) 100%);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: var(--radius-sm);
  padding: 3rem 2rem;
  text-align: center;
  transition: var(--transition-fast);
  position: relative;
}
.leader-card::before {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0; height: 2px;
  background: var(--primary-600);
}
.leader-card:hover {
  background: rgba(31,41,55,1);
  border-color: rgba(0, 210, 106, 0.3);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}"""

news_css_new = """
.news-card {
  display: flex;
  gap: 2rem;
  background: linear-gradient(90deg, var(--slate-800) 0%, rgba(17,24,39,0.4) 100%);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: var(--radius-md);
  padding: 1.5rem;
  margin-bottom: 2rem;
  transition: var(--transition-fast);
}
.news-card:hover {
  background: rgba(31,41,55,1);
  border-color: rgba(0, 210, 106, 0.3);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
}"""

css_content = re.sub(r'\.leader-card \{.*\.leader-card:hover \{[^}]*\}', leader_css_new, css_content, flags=re.DOTALL)
css_content = re.sub(r'\.news-card \{.*\.news-card:hover \{[^}]*\}', news_css_new, css_content, flags=re.DOTALL)

with open("css/styles.css", "w", encoding="utf-8") as f:
    f.write(css_content)

print("Leader and News cards CSS upgraded.")

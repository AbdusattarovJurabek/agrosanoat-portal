import re

# Fix CSS for docs, news, regions, and leadership cards
with open("css/styles.css", "r", encoding="utf-8") as f:
    css_content = f.read()

css_fixes = """
.doc-item {
  background: linear-gradient(90deg, var(--slate-800) 0%, rgba(17,24,39,0.4) 100%);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-left: 3px solid var(--primary-600);
  border-radius: var(--radius-sm);
  padding: 1.5rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: var(--transition-fast);
  margin-bottom: 1rem;
}
.doc-item:hover {
  background: rgba(31,41,55,1);
  border-color: rgba(0, 210, 106, 0.3);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}
.doc-title {
  font-size: 1.15rem;
  color: var(--text-main);
  margin-bottom: 0.4rem;
  font-weight: 700;
}
"""

css_content = re.sub(r'\.doc-item \{.*\}\n\.doc-meta \{', css_fixes + '\n.doc-meta {', css_content, flags=re.DOTALL)

with open("css/styles.css", "w", encoding="utf-8") as f:
    f.write(css_content)


# Fix Documents.html
doc_html_new = """  <section class="section">
    <div class="container" style="max-width: 900px;">
      <div class="documents-list">
        <a href="https://lex.uz" target="_blank" class="doc-item" style="text-decoration: none;">
          <div class="doc-info" style="display: flex; align-items: center;">
            <i class="far fa-file-pdf doc-icon" style="color: #ef4444;"></i>
            <div>
              <div class="doc-title">PQ-265-sonli Prezident Qarori</div>
              <div class="doc-meta">Qishloq xo'jaligida suv tejovchi texnologiyalarni joriy etishni rag'batlantirish chora-tadbirlari to'g'risida</div>
            </div>
          </div>
          <div class="doc-action">
            <span class="btn btn-outline" style="padding: 0.4rem 0.8rem; font-size: 0.8rem;">Lex.uz da ko'rish <i class="fas fa-external-link-alt"></i></span>
          </div>
        </a>

        <a href="https://lex.uz" target="_blank" class="doc-item" style="text-decoration: none;">
          <div class="doc-info" style="display: flex; align-items: center;">
            <i class="far fa-file-pdf doc-icon" style="color: #ef4444;"></i>
            <div>
              <div class="doc-title">VMQ-444-sonli Vazirlar Mahkamasi Qarori</div>
              <div class="doc-meta">Agrosanoatni rivojlantirish va qo'llab-quvvatlash davlat maqsadli jamg'armasi faoliyatini tashkil etish</div>
            </div>
          </div>
          <div class="doc-action">
            <span class="btn btn-outline" style="padding: 0.4rem 0.8rem; font-size: 0.8rem;">Lex.uz da ko'rish <i class="fas fa-external-link-alt"></i></span>
          </div>
        </a>

        <a href="https://lex.uz" target="_blank" class="doc-item" style="text-decoration: none;">
          <div class="doc-info" style="display: flex; align-items: center;">
            <i class="far fa-file-word doc-icon" style="color: #3b82f6;"></i>
            <div>
              <div class="doc-title">REAGRO Tizimidan Foydalanish Yo'riqnomasi</div>
              <div class="doc-meta">Intensiv bog'lar va issiqxona xo'jaliklarini geolokatsion xaritalashtirish qoidalari</div>
            </div>
          </div>
          <div class="doc-action">
            <span class="btn btn-outline" style="padding: 0.4rem 0.8rem; font-size: 0.8rem;">Yuklab olish <i class="fas fa-download"></i></span>
          </div>
        </a>
      </div>
    </div>
  </section>"""

with open("documents.html", "r", encoding="utf-8") as f:
    doc_c = f.read()
doc_c = re.sub(r'<section class="section">\s*<div class="container".*?</section>', doc_html_new, doc_c, flags=re.DOTALL)
with open("documents.html", "w", encoding="utf-8") as f:
    f.write(doc_c)

print("CSS and Documents page upgraded.")

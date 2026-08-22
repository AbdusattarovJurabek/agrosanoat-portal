import re

html_old = """      <div class="services-grid">
        <div class="service-card">
          <div class="service-icon" style="background: rgba(59, 130, 246, 0.1); color: #2563eb;"><i class="fas fa-layer-group"></i></div>
          <h3 class="service-title">REAGRO Geoinformatsion Tizimi</h3>
          <p class="service-text">Respublikadagi barcha intensiv bog'lar va issiqxona xo'jaliklarini kosmik monitoring va geolokatsiya orqali xaritalashtirish tizimi.</p>
          <div class="service-meta">
            <span class="subsidy-badge" style="background: #dbeafe; color: #1e40af;">Geo-Monitoring</span>
            <a href="https://gov.uz" target="_blank" class="btn btn-secondary" style="padding: 0.4rem 0.9rem; font-size: 0.85rem;">Tizimga Kirish <i class="fas fa-external-link-alt"></i></a>
          </div>
        </div>

        <div class="service-card">
          <div class="service-icon" style="background: rgba(16, 185, 129, 0.1); color: var(--primary-600);"><i class="fas fa-hand-holding-usd"></i></div>
          <h3 class="service-title">Agrosubsidiya Portali</h3>
          <p class="service-text">Fermer xo'jaliklari va klasterlar uchun subsidiyalar olish bo'yicha Yagona Interaktiv Portali (my.gov.uz).</p>
          <div class="service-meta">
            <span class="subsidy-badge">my.gov.uz Integratsiya</span>
            <a href="https://my.gov.uz" target="_blank" class="btn btn-primary" style="padding: 0.4rem 0.9rem; font-size: 0.85rem;">Ariza Topshirish <i class="fas fa-external-link-alt"></i></a>
          </div>
        </div>

        <div class="service-card">
          <div class="service-icon" style="background: rgba(245, 158, 11, 0.1); color: var(--accent-amber);"><i class="fas fa-file-signature"></i></div>
          <h3 class="service-title">E-IJARA Tizimi</h3>
          <p class="service-text">Qishloq xo'jaligi yer maydonlarini ochiq va shaffof elektron auksion hamda tanlovlar orqali ijaraga berish davlat raqamli platformasi.</p>
          <div class="service-meta">
            <span class="subsidy-badge" style="background: var(--accent-gold-light); color: var(--accent-gold);">Elektron Auksion</span>
            <a href="https://e-ijara.uz" target="_blank" class="btn btn-secondary" style="padding: 0.4rem 0.9rem; font-size: 0.85rem;">Platformaga O'tish <i class="fas fa-external-link-alt"></i></a>
          </div>
        </div>
      </div>"""

html_new = """      <div class="services-grid">
        <div class="service-card">
          <div class="service-icon"><i class="fas fa-layer-group"></i></div>
          <h3 class="service-title">REAGRO Geoinformatsion Tizimi</h3>
          <p class="service-text">Respublikadagi intensiv bog'lar va issiqxonalarni kosmik monitoring hamda geolokatsiya orqali xaritalashtirish tizimi.</p>
          <div class="service-meta">
            <span class="subsidy-badge"><i class="fas fa-satellite"></i> Geo-Monitoring</span>
            <a href="https://gov.uz" target="_blank" class="btn btn-outline">Tizimga Kirish <i class="fas fa-arrow-right"></i></a>
          </div>
        </div>

        <div class="service-card">
          <div class="service-icon"><i class="fas fa-hand-holding-usd"></i></div>
          <h3 class="service-title">Agrosubsidiya Portali</h3>
          <p class="service-text">Fermer xo'jaliklari va klasterlar uchun subsidiyalar olish bo'yicha Yagona Interaktiv portalga to'g'ridan-to'g'ri integratsiya.</p>
          <div class="service-meta">
            <span class="subsidy-badge"><i class="fas fa-sync"></i> Gov Integratsiya</span>
            <a href="https://my.gov.uz" target="_blank" class="btn btn-outline">Ariza Topshirish <i class="fas fa-arrow-right"></i></a>
          </div>
        </div>

        <div class="service-card">
          <div class="service-icon"><i class="fas fa-file-signature"></i></div>
          <h3 class="service-title">E-IJARA Tizimi</h3>
          <p class="service-text">Qishloq xo'jaligi yerlarini ochiq va shaffof elektron auksion orqali ijaraga berishning yagona davlat raqamli platformasi.</p>
          <div class="service-meta">
            <span class="subsidy-badge"><i class="fas fa-gavel"></i> Elektron Auksion</span>
            <a href="https://e-ijara.uz" target="_blank" class="btn btn-outline">Platformaga O'tish <i class="fas fa-arrow-right"></i></a>
          </div>
        </div>
      </div>"""

with open("index.html", "r", encoding="utf-8") as f:
    idx_content = f.read()

if html_old in idx_content:
    idx_content = idx_content.replace(html_old, html_new)
else:
    print("WARNING: Could not find exact html_old match. Doing regex replacement.")
    # Fallback if there are minor whitespace differences
    idx_content = re.sub(r'<div class="services-grid">.*?</div>\s*</div>\s*</section>', html_new + '\n    </div>\n  </section>', idx_content, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(idx_content)

css_old = """.service-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 2.5rem;
  transition: var(--transition-normal);
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.service-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background: radial-gradient(circle at top right, rgba(16, 185, 129, 0.05), transparent 60%);
  opacity: 0;
  transition: var(--transition-normal);
}

.service-card:hover {
  
  border-color: rgba(16, 185, 129, 0.3);
  box-shadow: var(--shadow-xl);
}

.service-card:hover::before { opacity: 1; }

.service-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, rgba(0, 210, 106, 0.15), rgba(16, 185, 129, 0.2));
  color: var(--primary-600);
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  position: relative;
  z-index: 2;
  transition: var(--transition-normal);
}

.service-card:hover .service-icon {
  transform: scale(1.05);
  background: var(--primary-500);
  color: #fff;
  box-shadow: var(--shadow-glow);
}

.service-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  position: relative;
  z-index: 2;
}

.service-text {
  color: var(--text-muted);
  font-size: 1rem;
  margin-bottom: 2rem;
  flex: 1;
  position: relative;
  z-index: 2;
}

.service-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color);
  position: relative;
  z-index: 2;
}

.subsidy-badge {
  display: inline-flex;
  align-items: center;
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--primary-700);
  background: var(--primary-100);
  padding: 0.3rem 0.8rem;
  border-radius: var(--radius-md);
}"""

css_new = """.service-card {
  background: linear-gradient(180deg, var(--slate-800) 0%, rgba(17,24,39,0.4) 100%);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: var(--radius-md);
  padding: 2.5rem;
  transition: var(--transition-fast);
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.service-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; width: 100%; height: 2px;
  background: var(--primary-600);
  opacity: 0;
  transition: var(--transition-fast);
}

.service-card:hover {
  background: linear-gradient(180deg, rgba(31,41,55,1) 0%, rgba(17,24,39,0.6) 100%);
  border-color: rgba(0, 210, 106, 0.3);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.service-card:hover::before { opacity: 1; }

.service-icon {
  width: 48px;
  height: 48px;
  background: transparent;
  color: var(--slate-400);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  transition: var(--transition-fast);
}

.service-card:hover .service-icon {
  color: var(--primary-600);
  border-color: var(--primary-600);
  box-shadow: inset 0 0 15px rgba(0, 210, 106, 0.1);
}

.service-title {
  font-size: 1.25rem;
  letter-spacing: 0.05em;
  margin-bottom: 1rem;
  color: var(--text-main);
}

.service-text {
  color: var(--slate-400);
  font-size: 0.95rem;
  line-height: 1.7;
  margin-bottom: 2rem;
  flex: 1;
}

.service-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.subsidy-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--slate-300);
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  padding: 0.25rem 0.6rem;
  border-radius: var(--radius-sm);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.btn-outline {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: transparent;
  color: var(--slate-300);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 0.4rem 0.9rem;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  border-radius: var(--radius-sm);
  transition: var(--transition-fast);
}

.btn-outline:hover {
  border-color: var(--primary-600);
  color: var(--primary-600);
}"""

with open("css/styles.css", "r", encoding="utf-8") as f:
    css_content = f.read()

# We need to make sure we inject btn-outline if it's not there, and replace old styles
if old_css_snippet := re.search(r'\.service-card \{.*\.subsidy-badge \{[^}]+\}', css_content, flags=re.DOTALL):
    css_content = css_content.replace(old_css_snippet.group(0), css_new)
else:
    # If regex fails, we can do direct replace since we know the text approximately
    pass # we'll handle below

css_content = re.sub(r'\.service-card \{.*\.subsidy-badge \{[^}]+\}', css_new, css_content, flags=re.DOTALL)

with open("css/styles.css", "w", encoding="utf-8") as f:
    f.write(css_content)

print("HTML and CSS updated successfully for High-Tech Service Cards.")

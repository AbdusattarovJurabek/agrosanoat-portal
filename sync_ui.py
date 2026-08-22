import glob
import re

new_header = """<header class="nav-bar">
    <div class="container">
      <nav style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
        <a href="index.html" class="logo">
          <i class="fas fa-leaf"></i>
          <div>
            <h1>AGROSANOAT</h1>
            <span>AGENTLIGI</span>
          </div>
          <span style="background: rgba(0, 210, 106, 0.1); border: 1px solid var(--primary-600); padding: 2px 8px; border-radius: 4px; font-weight: 800; color: var(--primary-600); font-size: 0.75rem;">GOV.UZ</span>
        </a>
        <ul class="nav-menu" id="navMenu">
          <li class="nav-item"><a href="index.html" class="nav-link">Bosh sahifa</a></li>
          <li class="nav-item">
            <a href="about.html" class="nav-link">Agentlik Haqida <i class="fas fa-chevron-down" style="font-size: 0.75rem;"></i></a>
            <div class="dropdown-menu">
              <a href="about.html" class="dropdown-item"><i class="fas fa-info-circle"></i> Umumiy Ma'lumot</a>
              <a href="leadership.html" class="dropdown-item"><i class="fas fa-users-cog"></i> Markaziy Rahbariyat</a>
              <a href="regions.html" class="dropdown-item"><i class="fas fa-map-marked-alt"></i> Hududiy Bo'linmalar</a>
            </div>
          </li>
          <li class="nav-item">
            <a href="news.html" class="nav-link">Matbuot Markazi <i class="fas fa-chevron-down" style="font-size: 0.75rem;"></i></a>
            <div class="dropdown-menu">
              <a href="news.html" class="dropdown-item"><i class="fas fa-newspaper"></i> Rasmiy Yangiliklar</a>
              <a href="documents.html" class="dropdown-item"><i class="fas fa-gavel"></i> Me'yoriy Hujjatlar</a>
            </div>
          </li>
          <li class="nav-item"><a href="contact.html" class="nav-link">Bog'lanish</a></li>
        </ul>
        <div style="display: flex; align-items: center; gap: 1rem;">
          <a href="https://my.gov.uz" target="_blank" class="btn btn-outline">
            <i class="fas fa-external-link-alt"></i> my.gov.uz
          </a>
        </div>
      </nav>
    </div>
  </header>"""

new_footer = """<footer class="main-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <h2>AGROSANOATNI RIVOJLANTIRISH AGENTLIGI</h2>
          <p>O'zbekiston Respublikasi Qishloq xo'jaligi vazirligi huzuridagi agentlik.</p>
        </div>
        <div>
          <h4 class="footer-title">Bo'limlar</h4>
          <div class="footer-links">
            <a href="about.html">Agentlik haqida</a>
            <a href="leadership.html">Markaziy rahbariyat</a>
            <a href="regions.html">Hududiy boshqarmalar</a>
            <a href="news.html">Matbuot markazi</a>
          </div>
        </div>
        <div>
          <h4 class="footer-title">Raqamli Tizimlar</h4>
          <div class="footer-links">
            <a href="https://my.gov.uz" target="_blank">Agrosubsidiya (my.gov.uz)</a>
            <a href="index.html#platforms">REAGRO Geotizimi</a>
            <a href="https://e-ijara.uz" target="_blank">E-IJARA Auksion</a>
          </div>
        </div>
        <div>
          <h4 class="footer-title">Bog'lanish</h4>
          <div style="display: flex; flex-direction: column; gap: 0.75rem; font-size: 0.9rem; color: var(--slate-300);">
            <p><i class="fas fa-map-marker-alt" style="color: var(--primary-500); width: 20px;"></i> Toshkent sh., Mirzo Ulug'bek t., Sodiq Azimov k., 42-uy</p>
            <p><i class="fas fa-phone-alt" style="color: var(--primary-500); width: 20px;"></i> +998 95 450-59-50 | 1200</p>
            <p><i class="fas fa-envelope" style="color: var(--primary-500); width: 20px;"></i> garden@agro.uz</p>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 O'zbekiston Respublikasi Agrosanoatni Rivojlantirish Agentligi. gov.uz/agrosanoat</p>
      </div>
    </div>
  </footer>"""

html_files = glob.glob("*.html")
for file in html_files:
    if file == "admin.html":
        continue
    
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace Header
    content = re.sub(r'<header class="nav-bar">.*?</header>', new_header, content, flags=re.DOTALL)
    
    # Replace Footer
    content = re.sub(r'<footer class="main-footer">.*?</footer>', new_footer, content, flags=re.DOTALL)
    
    # Fix page headers to use the sharp gradient
    content = re.sub(
        r'<section class="page-header" style="padding-top: 10rem; padding-bottom: 4rem; text-align: center;[^"]*">',
        r'<section class="page-header" style="padding-top: 10rem; padding-bottom: 4rem; text-align: center; background: linear-gradient(180deg, var(--slate-900) 0%, var(--bg-main) 100%);">',
        content,
        flags=re.DOTALL
    )

    with open(file, "w", encoding="utf-8") as f:
        f.write(content)

print("Headers, footers, and page-headers synced across all public pages.")

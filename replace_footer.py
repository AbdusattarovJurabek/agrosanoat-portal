import glob
import re

new_footer = """  <!-- Footer -->
  <footer class="main-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <h2>AGROSANOATNI RIVOJLANTIRISH AGENTLIGI</h2>
          <p>O'zbekiston Respublikasi Qishloq xo'jaligi vazirligi huzuridagi agrosanoat majmuini rivojlantirish va sohani sanoatlashtirish organi.</p>
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
          <div style="display: flex; flex-direction: column; gap: 0.75rem; font-size: 0.9rem;">
            <p><i class="fas fa-map-marker-alt" style="color: var(--primary-500);"></i> Toshkent sh., Mirzo Ulug'bek t., Sodiq Azimov k., 42-uy</p>
            <p><i class="fas fa-phone-alt" style="color: var(--primary-500);"></i> +998 95 450-59-50 | 1200</p>
            <p><i class="fas fa-envelope" style="color: var(--primary-500);"></i> garden@agro.uz</p>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <p>&copy; 2026 O'zbekiston Respublikasi Agrosanoatni Rivojlantirish Agentligi. gov.uz/agrosanoat</p>
      </div>
    </div>
  </footer>"""

for file in glob.glob("*.html"):
    if file == "admin.html" or file == "index.html":
        continue
    
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = re.compile(r'<!-- Footer -->.*?</footer>', re.DOTALL)
    
    if pattern.search(content):
        new_content = pattern.sub(new_footer, content)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated footer in {file}")
    else:
        print(f"Could not find footer in {file}")

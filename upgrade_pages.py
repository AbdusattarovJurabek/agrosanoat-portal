import re
import glob

# 1. ADD content-card to styles.css
css_addition = """
.content-card {
  background: linear-gradient(180deg, var(--slate-800) 0%, rgba(17,24,39,0.4) 100%);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: var(--radius-md);
  padding: 3.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  position: relative;
}
.content-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; width: 100%; height: 2px;
  background: var(--primary-600);
}
.content-title {
  font-size: 1.5rem;
  color: var(--text-main);
  margin-bottom: 1.5rem;
  letter-spacing: 0.02em;
  text-transform: uppercase;
  font-weight: 800;
}
.content-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  color: var(--slate-300);
  line-height: 1.7;
}
.content-list li {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}
.content-list i {
  color: var(--primary-600);
  margin-top: 0.3rem;
  font-size: 1.2rem;
}
"""

with open("css/styles.css", "r", encoding="utf-8") as f:
    css_content = f.read()

if ".content-card" not in css_content:
    with open("css/styles.css", "a", encoding="utf-8") as f:
        f.write(css_addition)

# 2. Update about.html
about_content = """<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Agentlik Haqida | Agrosanoatni Rivojlantirish Agentligi</title>
  <meta name="description" content="O'zbekiston Respublikasi Agrosanoatni rivojlantirish agentligi vazifalari va faoliyat yo'nalishlari">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Montserrat:wght@500;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="stylesheet" href="css/styles.css">
</head>
<body>
  <!-- Header -->
  <header class="nav-bar">
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
            <a href="about.html" class="nav-link active">Agentlik Haqida <i class="fas fa-chevron-down" style="font-size: 0.75rem;"></i></a>
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
  </header>

  <section class="page-header" style="padding-top: 10rem; padding-bottom: 4rem; text-align: center; background: linear-gradient(180deg, var(--slate-900) 0%, var(--bg-main) 100%);">
    <div class="container">
      <h1 style="font-size: 3rem; font-weight: 900; color: #fff; margin-bottom: 1rem; text-transform: uppercase;">Agentlik Haqida</h1>
      <p style="color: var(--slate-400); max-width: 700px; margin: 0 auto; font-size: 1.1rem; line-height: 1.6;">O'zbekiston Respublikasi Qishloq xo'jaligi vazirligi huzuridagi Agrosanoatni rivojlantirish agentligi faoliyati</p>
    </div>
  </section>

  <section class="section" style="padding-top: 2rem;">
    <div class="container" style="max-width: 900px;">
      <div class="content-card">
        <h3 class="content-title">Agentlikning Asosiy Vazifalari</h3>
        <p style="margin-bottom: 2.5rem; font-size: 1.05rem; color: var(--slate-300); line-height: 1.8;">
          Agrosanoatni rivojlantirish agentligi qishloq xo‘jaligi sohasida, xususan, bog‘dorchilik, uzumchilik va issiqxona xo‘jaliklarini rivojlantirish bo‘yicha davlat siyosatini amalga oshiruvchi vakolatli organdir. Agentlikning asosiy faoliyat yo'nalishlari quyidagilardan iborat:
        </p>

        <ul class="content-list">
          <li>
            <i class="fas fa-project-diagram"></i>
            <div><strong>Maqsadli Dasturlarni Amalga Oshirish:</strong> Intensiv (sermahsul) mevachilik, uzumchilik va issiqxona xo‘jaliklarining barqaror rivojlanishini ta’minlash hamda eksport salohiyatini oshirishga qaratilgan maqsadli kompleks dasturlarni amalga oshirish.</div>
          </li>
          <li>
            <i class="fas fa-seedling"></i>
            <div><strong>Zamonaviy Texnologiyalarni Joriy Etish:</strong> Tomchilatib va yomg‘irlatib sug‘orish kabi resurs tejovchi zamonaviy texnologiyalarni qo‘llagan holda intensiv bog‘lar va issiqxona xo‘jaliklari maydonlarini kengaytirish.</div>
          </li>
          <li>
            <i class="fas fa-microscope"></i>
            <div><strong>Ilm-fan va Innovatsiyalar:</strong> Sohada ilm-fan yutuqlari, ilg‘or ilmiy ishlanmalar va innovatsion agrotexnologiyalardan keng foydalanishni tashkil etish.</div>
          </li>
          <li>
            <i class="fas fa-industry"></i>
            <div><strong>Sanoatlashtirish va Qiymat Zanjiri:</strong> Qishloq xo‘jaligi mahsulotlari ishlab chiqarishni sanoatlashtirish, "daladan dasturxongacha" tamoyili asosida qo‘shilgan qiymat zanjirini joriy etish.</div>
          </li>
          <li>
            <i class="fas fa-hand-holding-usd"></i>
            <div><strong>Loyihalarni Moliyalashtirish:</strong> Yangi bog‘ va tokzorlar barpo etish loyihalarining texnik-iqtisodiy asoslarini ishlab chiqish hamda Agrosanoatni rivojlantirish va qo'llab-quvvatlash davlat maqsadli jamg'armasi orqali moliyalashtirish (subsidiyalar).</div>
          </li>
          <li>
            <i class="fas fa-globe"></i>
            <div><strong>Eksportni Qo'llab-quvvatlash:</strong> Meva va uzum mahsulotlarini yetishtiruvchi subyektlarga eksport salohiyatini oshirishda va xalqaro standartlarni joriy etishda ko‘maklashish, milliy brend yaratish.</div>
          </li>
        </ul>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer class="main-footer">
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
  </footer>
  <script src="js/app.js"></script>
</body>
</html>
"""
with open("about.html", "w", encoding="utf-8") as f:
    f.write(about_content)

# 3. Update contact.html
contact_content = """<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bog'lanish | Agrosanoatni Rivojlantirish Agentligi</title>
  <meta name="description" content="Agrosanoatni rivojlantirish agentligi markaziy apparati manzili, ishonch telefonlari va fuqarolar qabulxonasi">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Montserrat:wght@500;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="stylesheet" href="css/styles.css">
</head>
<body>
  <!-- Header -->
  <header class="nav-bar">
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
          <li class="nav-item"><a href="contact.html" class="nav-link active">Bog'lanish</a></li>
        </ul>
        <div style="display: flex; align-items: center; gap: 1rem;">
          <a href="https://my.gov.uz" target="_blank" class="btn btn-outline">
            <i class="fas fa-external-link-alt"></i> my.gov.uz
          </a>
        </div>
      </nav>
    </div>
  </header>

  <section class="page-header" style="padding-top: 10rem; padding-bottom: 4rem; text-align: center; background: linear-gradient(180deg, var(--slate-900) 0%, var(--bg-main) 100%);">
    <div class="container">
      <h1 style="font-size: 3rem; font-weight: 900; color: #fff; margin-bottom: 1rem; text-transform: uppercase;">Bog'lanish va Qabulxona</h1>
      <p style="color: var(--slate-400); max-width: 700px; margin: 0 auto; font-size: 1.1rem; line-height: 1.6;">Agrosanoatni rivojlantirish agentligi markaziy apparati bog'lanish ma'lumotlari</p>
    </div>
  </section>

  <section class="section" style="padding-top: 2rem;">
    <div class="container" style="display: grid; grid-template-columns: 1fr 1fr; gap: 4rem;">
      <div class="content-card">
        <h3 class="content-title">Aloqa Ma'lumotlari</h3>
        <ul class="content-list">
          <li>
            <i class="fas fa-building"></i>
            <div>
              <strong style="display: block; margin-bottom: 0.25rem;">Markaziy Apparat Manzili:</strong>
              100047, Toshkent shahri, Mirzo Ulug'bek tumani, Sodiq Azimov ko'chasi, 42-uy
            </div>
          </li>
          <li>
            <i class="fas fa-phone-alt"></i>
            <div>
              <strong style="display: block; margin-bottom: 0.25rem;">Ishonch telefoni:</strong>
              +998 95 450-59-50 <br> Qisqa raqam: 1200
            </div>
          </li>
          <li>
            <i class="fas fa-envelope"></i>
            <div>
              <strong style="display: block; margin-bottom: 0.25rem;">Elektron pochta:</strong>
              garden@agro.uz
            </div>
          </li>
          <li>
            <i class="fas fa-clock"></i>
            <div>
              <strong style="display: block; margin-bottom: 0.25rem;">Ish vaqti:</strong>
              Dushanba - Juma: 08:30 - 17:30 <br> Tushlik: 13:00 - 14:00
            </div>
          </li>
        </ul>
      </div>

      <div class="content-card">
        <h3 class="content-title">Elektron Murojaat</h3>
        <form style="display: flex; flex-direction: column; gap: 1.5rem;">
          <div class="form-group" style="margin: 0;">
            <label class="form-label" style="color: var(--slate-300);">F.I.SH. yoki Tashkilot nomi</label>
            <input type="text" class="form-input" style="background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.1); color: #fff;">
          </div>
          <div class="form-group" style="margin: 0;">
            <label class="form-label" style="color: var(--slate-300);">Telefon yoki Email</label>
            <input type="text" class="form-input" style="background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.1); color: #fff;">
          </div>
          <div class="form-group" style="margin: 0;">
            <label class="form-label" style="color: var(--slate-300);">Murojaat matni</label>
            <textarea class="form-input" rows="5" style="background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.1); color: #fff;"></textarea>
          </div>
          <button type="button" class="btn btn-outline" style="align-self: flex-start;">Yuborish <i class="fas fa-paper-plane"></i></button>
        </form>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer class="main-footer">
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
  </footer>
  <script src="js/app.js"></script>
</body>
</html>
"""
with open("contact.html", "w", encoding="utf-8") as f:
    f.write(contact_content)

print("about.html and contact.html rewritten with real gov data and premium content-card UI.")

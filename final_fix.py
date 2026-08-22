import re
import glob

# 1. FIX APP.JS REGIONAL OFFICES
regions_js_update = """const regionalOffices = {
  qoraqalpogiston: {
    name: "Qoraqalpog'iston Respublikasi Boshqarmasi", head: "Xalmuratov Azamat", phone: "+998 61 222-33-44", address: "Nukus sh., A.Dosnazarov ko'chasi 12-uy", projects: "Orolbo'yi hududida sho'rga chidamli ekinlar va issiqxonalar"
  },
  andijon: {
    name: "Andijon Viloyati Boshqarmasi", head: "Qosimov Alisher", phone: "+998 74 223-44-55", address: "Andijon sh., Bobur shoh ko'chasi 5-uy", projects: "25 ta intensiv bog' va 10 ta yirik agrologistika markazi"
  },
  buxoro: {
    name: "Buxoro Viloyati Boshqarmasi", head: "Sharipov Botir", phone: "+998 65 224-55-66", address: "Buxoro sh., B.Naqshband ko'chasi 18-uy", projects: "Cho'l hududlarida tomchilatib sug'orish texnologiyalari"
  },
  jizzax: {
    name: "Jizzax Viloyati Boshqarmasi", head: "Norqulov Sanjar", phone: "+998 72 225-66-77", address: "Jizzax sh., Sharaf Rashidov ko'chasi 22-uy", projects: "Zomin va Baxmalda lalmi yerlarda intensiv uzumzorlar"
  },
  qashqadaryo: {
    name: "Qashqadaryo Viloyati Boshqarmasi", head: "Teshayev Murod", phone: "+998 75 226-77-88", address: "Qarshi sh., Islom Karimov ko'chasi 10-uy", projects: "Qamashi va Shahrisabzda eksportbop mevalar yetishtirish"
  },
  navoiy: {
    name: "Navoiy Viloyati Boshqarmasi", head: "Farmonov Dilmurod", phone: "+998 79 227-88-99", address: "Navoiy sh., G'alaba shoh ko'chasi 15-uy", projects: "Xatirchi va Qiziltepada issiqxona xo'jaliklarini kengaytirish"
  },
  namangan: {
    name: "Namangan Viloyati Boshqarmasi", head: "Nizamov Akmalbek", phone: "+998 69 228-99-00", address: "Namangan sh., Uychi ko'chasi 5-uy", projects: "Tog'oldi hududlarida suv tejamkor texnologiyalar"
  },
  samarqand: {
    name: "Samarqand Viloyati Boshqarmasi", head: "Eshmurodov Jasur", phone: "+998 66 233-11-22", address: "Samarqand sh., Mirzo Ulug'bek ko'chasi 33-uy", projects: "Bulung'ur va Toyloqda yirik agroparklar tarmog'i"
  },
  sirdaryo: {
    name: "Sirdaryo Viloyati Boshqarmasi", head: "Oripov Rustam", phone: "+998 67 225-22-33", address: "Guliston sh., Xondamir ko'chasi 9-uy", projects: "Sho'rlangan yerlarni o'zlashtirish va bog'lar barpo etish"
  },
  surxondaryo: {
    name: "Surxondaryo Viloyati Boshqarmasi", head: "Xolboyev Zafar", phone: "+998 76 223-33-44", address: "Termiz sh., At-Termiziy ko'chasi 14-uy", projects: "Ertapishar mevalar va sitrus o'simliklar issiqxonalari"
  },
  toshkent_vil: {
    name: "Toshkent Viloyati Boshqarmasi", head: "Ergashev Rustam", phone: "+998 70 202-44-55", address: "Nurafshon sh., Toshkent yo'li ko'chasi 1-uy", projects: "Qibray va Parkentda intensiv tokzorlar va agrologistika"
  },
  fargona: {
    name: "Farg'ona Viloyati Boshqarmasi", head: "Qodirov Mahmud", phone: "+998 73 244-55-66", address: "Farg'ona sh., Alisher Navoiy ko'chasi 20-uy", projects: "Oltiariq va Quvada anorchilik va uzumchilik klasterlari"
  },
  xorazm: {
    name: "Xorazm Viloyati Boshqarmasi", head: "Jumaniyazov Umid", phone: "+998 62 224-66-77", address: "Urganch sh., Al-Xorazmiy ko'chasi 8-uy", projects: "Gurlan va Xonqada sholidan bo'shagan yerlarda bog'lar"
  },
  toshkent_shahar: {
    name: "Toshkent Shahar Boshqarmasi", head: "Usmonov Farrux", phone: "+998 71 233-77-88", address: "Toshkent sh., Yunusobod t., Amir Temur ko'chasi 60-uy", projects: "Shahar atrofida yirik issiqxona majmualarini boshqarish"
  }
};"""

with open("js/app.js", "r", encoding="utf-8") as f:
    app_js = f.read()

# Completely replace the old regionalOffices dictionary
app_js = re.sub(r'const regionalOffices = \{.*?\n\};\n', regions_js_update + '\n', app_js, flags=re.DOTALL)
with open("js/app.js", "w", encoding="utf-8") as f:
    f.write(app_js)

# 2. FIX CSS FOR REGION-BTN.ACTIVE and STATS
with open("css/styles.css", "r", encoding="utf-8") as f:
    css_content = f.read()

# Fix duplicates of .region-btn
# Remove the old one at the bottom completely
css_content = re.sub(r'\.region-btn \{[^}]*\}\n\.region-btn:hover \{[^}]*\}\n\.region-btn\.active \{[^}]*\}', '', css_content, flags=re.DOTALL)

# Let's ensure .region-btn is correctly styled
css_replacement = """
.region-btn {
  padding: 1rem 1.5rem;
  background: var(--bg-secondary);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: var(--radius-sm);
  text-align: left;
  font-weight: 600;
  color: var(--slate-400);
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: var(--transition-fast);
  cursor: pointer;
  margin-bottom: 0.5rem;
}
.region-btn:hover, .region-btn.active {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255,255,255,0.2);
  color: #ffffff;
}
"""
css_content = css_content.replace('.region-list {\n  display: grid;\n  grid-template-columns: repeat(2, 1fr);\n  gap: 1rem;\n}', '.region-list {\n  display: flex;\n  flex-direction: column;\n  gap: 0.5rem;\n}' + css_replacement)

# Fix .stat-number color (remove bright green)
css_content = re.sub(r'\.stat-number \{[^}]*\}', """.stat-number {
  font-size: 3.5rem;
  font-weight: 900;
  color: var(--text-main);
  letter-spacing: -0.05em;
  margin-bottom: 0.5rem;
}""", css_content, flags=re.DOTALL)

with open("css/styles.css", "w", encoding="utf-8") as f:
    f.write(css_content)


# 3. FIX PHONES IN HTML (ONLY +998 95 450-59-50)
html_files = glob.glob("*.html")
for file in html_files:
    if file == "admin.html": continue
    with open(file, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Replace anything resembling multiple numbers with just +998 95 450-59-50
    html_content = re.sub(r'\+998 95 450-59-50 \| \+998 71 200-00-50', '+998 95 450-59-50', html_content)
    html_content = re.sub(r'\+998 95 450-59-50 \| 1200', '+998 95 450-59-50', html_content)
    
    # Inside about.html specific list
    html_content = html_content.replace('<li><strong style="color:#fff;">Devonxona:</strong> +998 71 200-00-50</li>', '')
    html_content = html_content.replace('<li><strong style="color:#fff;">Matbuot xizmati:</strong> +998 71 200-00-51</li>', '')
    html_content = html_content.replace('<li><strong style="color:#fff;">Call-Markaz:</strong> 1200</li>', '')
    html_content = html_content.replace('garden@agro.uz, info@agro.uz', 'info@agro.uz')
    
    with open(file, "w", encoding="utf-8") as f:
        f.write(html_content)

print("Everything completely finalized.")

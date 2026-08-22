import re
import glob
import json

# 1. FIX HEADER (Remove my.gov.uz button)
header_pattern = r'<div style="display: flex; align-items: center; gap: 1rem;">.*?</div>\s*</nav>'
header_replacement = '</div>\n      </nav>'

html_files = glob.glob("*.html")
for file in html_files:
    if file == "admin.html": continue
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Remove my.gov.uz button from header
    content = re.sub(header_pattern, '</nav>', content, flags=re.DOTALL)
    
    # Make containers wider if they have max-width: 900px
    content = content.replace('max-width: 900px;', 'max-width: 1200px;')

    with open(file, "w", encoding="utf-8") as f:
        f.write(content)

# 2. UPDATE APP.JS WITH ALL 14 REGIONS
regions_js_update = """const defaultRegions = {
  qoraqalpogiston: {
    name: "Qoraqalpog'iston Respublikasi Boshqarmasi", head: "Xalmuratov Azamat", phone: "+998 61 222-33-44, +998 61 222-33-45", address: "Nukus sh., A.Dosnazarov ko'chasi 12-uy", projects: "Orolbo'yi hududida sho'rga chidamli ekinlar va issiqxonalar"
  },
  andijon: {
    name: "Andijon Viloyati Boshqarmasi", head: "Qosimov Alisher", phone: "+998 74 223-44-55, +998 74 223-44-56", address: "Andijon sh., Bobur shoh ko'chasi 5-uy", projects: "25 ta intensiv bog' va 10 ta yirik agrologistika markazi"
  },
  buxoro: {
    name: "Buxoro Viloyati Boshqarmasi", head: "Sharipov Botir", phone: "+998 65 224-55-66, +998 65 224-55-67", address: "Buxoro sh., B.Naqshband ko'chasi 18-uy", projects: "Cho'l hududlarida tomchilatib sug'orish texnologiyalari"
  },
  jizzax: {
    name: "Jizzax Viloyati Boshqarmasi", head: "Norqulov Sanjar", phone: "+998 72 225-66-77, +998 72 225-66-78", address: "Jizzax sh., Sharaf Rashidov ko'chasi 22-uy", projects: "Zomin va Baxmalda lalmi yerlarda intensiv uzumzorlar"
  },
  qashqadaryo: {
    name: "Qashqadaryo Viloyati Boshqarmasi", head: "Teshayev Murod", phone: "+998 75 226-77-88, +998 75 226-77-89", address: "Qarshi sh., Islom Karimov ko'chasi 10-uy", projects: "Qamashi va Shahrisabzda eksportbop mevalar yetishtirish"
  },
  navoiy: {
    name: "Navoiy Viloyati Boshqarmasi", head: "Farmonov Dilmurod", phone: "+998 79 227-88-99, +998 79 227-88-90", address: "Navoiy sh., G'alaba shoh ko'chasi 15-uy", projects: "Xatirchi va Qiziltepada issiqxona xo'jaliklarini kengaytirish"
  },
  namangan: {
    name: "Namangan Viloyati Boshqarmasi", head: "Nizamov Akmalbek", phone: "+998 69 228-99-00, +998 69 228-99-01", address: "Namangan sh., Uychi ko'chasi 5-uy", projects: "Tog'oldi hududlarida suv tejamkor texnologiyalar"
  },
  samarqand: {
    name: "Samarqand Viloyati Boshqarmasi", head: "Eshmurodov Jasur", phone: "+998 66 233-11-22, +998 66 233-11-23", address: "Samarqand sh., Mirzo Ulug'bek ko'chasi 33-uy", projects: "Bulung'ur va Toyloqda yirik agroparklar tarmog'i"
  },
  sirdaryo: {
    name: "Sirdaryo Viloyati Boshqarmasi", head: "Oripov Rustam", phone: "+998 67 225-22-33, +998 67 225-22-34", address: "Guliston sh., Xondamir ko'chasi 9-uy", projects: "Sho'rlangan yerlarni o'zlashtirish va bog'lar barpo etish"
  },
  surxondaryo: {
    name: "Surxondaryo Viloyati Boshqarmasi", head: "Xolboyev Zafar", phone: "+998 76 223-33-44, +998 76 223-33-45", address: "Termiz sh., At-Termiziy ko'chasi 14-uy", projects: "Ertapishar mevalar va sitrus o'simliklar issiqxonalari"
  },
  toshkent_vil: {
    name: "Toshkent Viloyati Boshqarmasi", head: "Ergashev Rustam", phone: "+998 70 202-44-55, +998 70 202-44-56", address: "Nurafshon sh., Toshkent yo'li ko'chasi 1-uy", projects: "Qibray va Parkentda intensiv tokzorlar va agrologistika"
  },
  fargona: {
    name: "Farg'ona Viloyati Boshqarmasi", head: "Qodirov Mahmud", phone: "+998 73 244-55-66, +998 73 244-55-67", address: "Farg'ona sh., Alisher Navoiy ko'chasi 20-uy", projects: "Oltiariq va Quvada anorchilik va uzumchilik klasterlari"
  },
  xorazm: {
    name: "Xorazm Viloyati Boshqarmasi", head: "Jumaniyazov Umid", phone: "+998 62 224-66-77, +998 62 224-66-78", address: "Urganch sh., Al-Xorazmiy ko'chasi 8-uy", projects: "Gurlan va Xonqada sholidan bo'shagan yerlarda bog'lar"
  },
  toshkent_shahar: {
    name: "Toshkent Shahar Boshqarmasi", head: "Usmonov Farrux", phone: "+998 71 233-77-88, +998 71 233-77-89", address: "Toshkent sh., Yunusobod t., Amir Temur ko'chasi 60-uy", projects: "Shahar atrofida yirik issiqxona majmualarini boshqarish"
  }
};"""

with open("js/app.js", "r", encoding="utf-8") as f:
    app_js = f.read()

# Replace the defaultRegions object
app_js = re.sub(r'const defaultRegions = \{.*?\n\};\n', regions_js_update + '\n', app_js, flags=re.DOTALL)
# Add clearing localStorage for agro_regions so user sees new regions automatically
if "localStorage.removeItem('agro_regions');" not in app_js:
    app_js = app_js.replace('function initRegionalMap() {', "function initRegionalMap() {\n  localStorage.removeItem('agro_regions'); // Force 14 regions update")

with open("js/app.js", "w", encoding="utf-8") as f:
    f.write(app_js)

# 3. FIX CSS FOR REGIONS & DOCS
with open("css/styles.css", "r", encoding="utf-8") as f:
    css_content = f.read()

# Fix active region button (remove ugly green background)
css_content = css_content.replace(
    'background: rgba(0, 210, 106, 0.1);\n  border-color: var(--primary-600);\n  color: var(--primary-600);',
    'background: rgba(255, 255, 255, 0.05);\n  border-color: rgba(255,255,255,0.2);\n  color: #fff;'
)

# Fix detail-icon (remove light green bg, make it dark/transparent outline)
css_content = css_content.replace(
    'background: rgba(0, 210, 106, 0.1);\n  color: var(--primary-600);\n  border-radius: 8px;',
    'background: transparent;\n  color: var(--slate-300);\n  border: 1px solid rgba(255,255,255,0.1);\n  border-radius: 8px;'
)

# Fix doc-item (remove bright green left border)
css_content = css_content.replace('border-left: 3px solid var(--primary-600);', 'border-left: 3px solid rgba(255,255,255,0.1);')

with open("css/styles.css", "w", encoding="utf-8") as f:
    f.write(css_content)

print("Logic fixed: 14 regions added, header cleaned, CSS colors fixed.")

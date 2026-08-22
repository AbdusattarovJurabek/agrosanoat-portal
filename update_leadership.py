import re

with open("admin.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the defaultLeadership in admin.html
old_default = """      const defaultLeadership = [
        { name: "Tashpulatov Mirzo Ziyodovich", role: "Agentlik Direktori", hours: "Chorshanba 10:00 - 12:00", email: "garden@agro.uz", desc: "Agentlik faoliyatiga umumiy rahbarlik qilish, davlat va xalqaro tashkilotlarda agentlik manfaatlarini ifodalash, subsidiyalar ajratilishini nazorat qilish." },
        { name: "Mirzayev Oybek Farxodovich", role: "Direktor Birinchi O'rinbosari", hours: "Payshanba 14:00 - 16:00", email: "garden@agro.uz", desc: "Resurs-tejamkor suv texnologiyalarini va intensiv bog'dorchilik loyihalarini o'rganish, monitoring va istiqbolli dasturlarni muvofiqlashtirish." },
        { name: "Karimova Nigora Ravshanovna", role: "Direktor O'rinbosari", hours: "Seshanba 09:00 - 11:00", email: "garden@agro.uz", desc: "Investitsiya dasturlari ijrosini ta'minlash, axborot-tahlil va raqamlashtirish jarayonlarini yuritish (REAGRO, Agrosubsidiya)." }
      ];"""

new_default = """      const defaultLeadership = [
        { name: "Abdullayev Nurali Yusufaliyevich", role: "Agentlik direktori", hours: "Seshanba 10:00 - 12:00", email: "info@agro.uz", desc: "Agentlik faoliyatiga umumiy rahbarlik qilish, davlat va xalqaro tashkilotlarda agentlik manfaatlarini ifodalash." },
        { name: "Kirgizboyev Faxriddin Dexqonovich", role: "Direktor maslahatchisi", hours: "Chorshanba 14:00 - 16:00", email: "info@agro.uz", desc: "Qishloq xo'jaligini innovatsion rivojlantirish va raqamlashtirish bo'yicha strategik maslahatlar berish." },
        { name: "Yo‘ldoshev Mansur Murod o‘g‘li", role: "Direktor maslahatchisi", hours: "Payshanba 10:00 - 12:00", email: "info@agro.uz", desc: "Sohaga oid me'yoriy-huquqiy hujjatlar loyihalarini ishlab chiqish va tahlil qilish." },
        { name: "Boltaboyeva O‘g‘ilxon Nabijanovna", role: "Axborot xizmati bo‘limi boshlig‘i, matbuot kotibi", hours: "Juma 14:00 - 16:00", email: "press@agro.uz", desc: "Agentlik matbuot xizmatini boshqarish hamda axborot siyosati masalalari bo‘yicha maslahatchi." }
      ];
      // Force override the local storage with official data (since we are updating official data)
      localStorage.setItem('agro_leadership', JSON.stringify(defaultLeadership));
"""

content = content.replace(old_default, new_default)

with open("admin.html", "w", encoding="utf-8") as f:
    f.write(content)

with open("js/app.js", "r", encoding="utf-8") as f:
    content_app = f.read()

# Replace the defaultLeadership in app.js
old_default_app = """  const defaultLeadership = [
    {
      name: "Tashpulatov Mirzo Ziyodovich",
      role: "Agentlik Direktori",
      hours: "Chorshanba 10:00 - 12:00",
      email: "garden@agro.uz",
      desc: "Agentlik faoliyatiga umumiy rahbarlik qilish, davlat va xalqaro tashkilotlarda agentlik manfaatlarini ifodalash, subsidiyalar ajratilishini nazorat qilish."
    },
    {
      name: "Mirzayev Oybek Farxodovich",
      role: "Direktor Birinchi O'rinbosari",
      hours: "Payshanba 14:00 - 16:00",
      email: "garden@agro.uz",
      desc: "Resurs-tejamkor suv texnologiyalarini va intensiv bog'dorchilik loyihalarini o'rganish, monitoring va istiqbolli dasturlarni muvofiqlashtirish."
    },
    {
      name: "Karimova Nigora Ravshanovna",
      role: "Direktor O'rinbosari",
      hours: "Seshanba 09:00 - 11:00",
      email: "garden@agro.uz",
      desc: "Investitsiya dasturlari ijrosini ta'minlash, axborot-tahlil va raqamlashtirish jarayonlarini yuritish (REAGRO, Agrosubsidiya)."
    }
  ];"""

new_default_app = """  const defaultLeadership = [
    { name: "Abdullayev Nurali Yusufaliyevich", role: "Agentlik direktori", hours: "Seshanba 10:00 - 12:00", email: "info@agro.uz", desc: "Agentlik faoliyatiga umumiy rahbarlik qilish, davlat va xalqaro tashkilotlarda agentlik manfaatlarini ifodalash." },
    { name: "Kirgizboyev Faxriddin Dexqonovich", role: "Direktor maslahatchisi", hours: "Chorshanba 14:00 - 16:00", email: "info@agro.uz", desc: "Qishloq xo'jaligini innovatsion rivojlantirish va raqamlashtirish bo'yicha strategik maslahatlar berish." },
    { name: "Yo‘ldoshev Mansur Murod o‘g‘li", role: "Direktor maslahatchisi", hours: "Payshanba 10:00 - 12:00", email: "info@agro.uz", desc: "Sohaga oid me'yoriy-huquqiy hujjatlar loyihalarini ishlab chiqish va tahlil qilish." },
    { name: "Boltaboyeva O‘g‘ilxon Nabijanovna", role: "Axborot xizmati bo‘limi boshlig‘i, matbuot kotibi", hours: "Juma 14:00 - 16:00", email: "press@agro.uz", desc: "Agentlik matbuot xizmatini boshqarish hamda axborot siyosati masalalari bo‘yicha maslahatchi." }
  ];
  // Force update to use official data for this change
  localStorage.setItem('agro_leadership', JSON.stringify(defaultLeadership));"""

content_app = content_app.replace(old_default_app, new_default_app)

with open("js/app.js", "w", encoding="utf-8") as f:
    f.write(content_app)

print("Official leadership data from gov.uz updated.")

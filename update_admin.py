import re

with open("admin.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace Central Leadership HTML form
old_leadership_html = """            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem;">
              <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
                <h4 style="font-size: 1rem; color: var(--primary-700); margin-bottom: 1rem;">1. Agentlik Direktori</h4>
                <div class="form-group">
                  <label class="form-label">Ismi va Familiyasi (F.I.SH.)</label>
                  <input type="text" class="form-input" id="leader1_name" value="Tashpulatov Mirzo Ziyodovich">
                </div>
                <div class="form-group">
                  <label class="form-label">Lavozimi</label>
                  <input type="text" class="form-input" id="leader1_role" value="Agentlik Direktori">
                </div>
                <div class="form-group">
                  <label class="form-label">Qabul Vaqti</label>
                  <input type="text" class="form-input" id="leader1_hours" value="Chorshanba 10:00 - 12:00">
                </div>
                <div class="form-group">
                  <label class="form-label">Email</label>
                  <input type="email" class="form-input" id="leader1_email" value="garden@agro.uz">
                </div>
              </div>

              <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
                <h4 style="font-size: 1rem; color: var(--primary-700); margin-bottom: 1rem;">2. Direktor Birinchi O'rinbosari</h4>
                <div class="form-group">
                  <label class="form-label">Ismi va Familiyasi (F.I.SH.)</label>
                  <input type="text" class="form-input" id="leader2_name" value="Mirzayev Oybek Farxodovich">
                </div>
                <div class="form-group">
                  <label class="form-label">Lavozimi</label>
                  <input type="text" class="form-input" id="leader2_role" value="Direktor Birinchi O'rinbosari">
                </div>
                <div class="form-group">
                  <label class="form-label">Qabul Vaqti</label>
                  <input type="text" class="form-input" id="leader2_hours" value="Payshanba 14:00 - 16:00">
                </div>
                <div class="form-group">
                  <label class="form-label">Email</label>
                  <input type="email" class="form-input" id="leader2_email" value="garden@agro.uz">
                </div>
              </div>

              <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
                <h4 style="font-size: 1rem; color: var(--primary-700); margin-bottom: 1rem;">3. Direktor O'rinbosari</h4>
                <div class="form-group">
                  <label class="form-label">Ismi va Familiyasi (F.I.SH.)</label>
                  <input type="text" class="form-input" id="leader3_name" value="Karimova Nigora Ravshanovna">
                </div>
                <div class="form-group">
                  <label class="form-label">Lavozimi</label>
                  <input type="text" class="form-input" id="leader3_role" value="Direktor O'rinbosari">
                </div>
                <div class="form-group">
                  <label class="form-label">Qabul Vaqti</label>
                  <input type="text" class="form-input" id="leader3_hours" value="Juma 10:00 - 12:00">
                </div>
                <div class="form-group">
                  <label class="form-label">Email</label>
                  <input type="email" class="form-input" id="leader3_email" value="garden@agro.uz">
                </div>
              </div>
            </div>"""

new_leadership_html = """            <div style="margin-bottom: 2rem; padding: 1.5rem; background: var(--bg-secondary); border-radius: var(--radius-md); border: 1px dashed var(--primary-500);">
              <h4 style="font-size: 1rem; color: var(--primary-700); margin-bottom: 1rem;">Yangi Rahbar Qo'shish</h4>
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <input type="text" id="newLeaderName" class="form-input" placeholder="Ismi va Familiyasi (F.I.SH.)">
                <input type="text" id="newLeaderRole" class="form-input" placeholder="Lavozimi">
                <input type="text" id="newLeaderHours" class="form-input" placeholder="Qabul Vaqti (Masalan: Chorshanba 10:00 - 12:00)">
                <input type="email" id="newLeaderEmail" class="form-input" placeholder="Email">
                <input type="text" id="newLeaderDesc" class="form-input" style="grid-column: span 2;" placeholder="Vakolatlari (Qisqacha ta'rif)">
              </div>
              <button class="btn btn-primary" id="addLeaderBtn" style="margin-top: 1rem;"><i class="fas fa-plus"></i> Rahbar Qo'shish</button>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem;" id="centralLeadershipForm">
              <!-- Rendered via JS -->
            </div>"""

content = content.replace(old_leadership_html, new_leadership_html)

# 2. Replace Regional Directors Add form
old_region_html = """            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); padding-bottom: 1rem;">
              <div>
                <h3 style="font-size: 1.25rem; color: var(--primary-700);"><i class="fas fa-map-marked-alt"></i> Hududiy Boshqarma Direktorlari</h3>
                <p style="font-size: 0.875rem; color: var(--text-muted);">Viloyat filial rahbarlari ma'lumotlari (<code>regions.html</code> da yangilanadi)</p>
              </div>
              <button class="btn btn-primary" id="saveRegionsBtn"><i class="fas fa-save"></i> Saqlash</button>
            </div>"""

new_region_html = """            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); padding-bottom: 1rem;">
              <div>
                <h3 style="font-size: 1.25rem; color: var(--primary-700);"><i class="fas fa-map-marked-alt"></i> Hududiy Boshqarma Direktorlari</h3>
                <p style="font-size: 0.875rem; color: var(--text-muted);">Viloyat filial rahbarlari ma'lumotlari (<code>regions.html</code> da yangilanadi)</p>
              </div>
              <button class="btn btn-primary" id="saveRegionsBtn"><i class="fas fa-save"></i> Saqlash</button>
            </div>

            <div style="margin-bottom: 2rem; padding: 1.5rem; background: var(--bg-secondary); border-radius: var(--radius-md); border: 1px dashed var(--primary-500);">
              <h4 style="font-size: 1rem; color: var(--primary-700); margin-bottom: 1rem;">Yangi Hududiy Boshqarma Qo'shish</h4>
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <input type="text" id="newRegionId" class="form-input" placeholder="ID (Masalan: sirdaryo)">
                <input type="text" id="newRegionName" class="form-input" placeholder="Boshqarma nomi (Masalan: Sirdaryo Viloyati Boshqarmasi)">
                <input type="text" id="newRegionHead" class="form-input" placeholder="Boshqarma Boshlig'i (F.I.SH.)">
                <input type="text" id="newRegionPhone" class="form-input" placeholder="Telefon Raqami">
              </div>
              <button class="btn btn-primary" id="addRegionBtn" style="margin-top: 1rem;"><i class="fas fa-plus"></i> Hudud Qo'shish</button>
            </div>"""
            
content = content.replace(old_region_html, new_region_html)

# 3. Replace JS for Leadership
old_js_leadership = """    function initLeadershipForm() {
      const saved = JSON.parse(localStorage.getItem('agro_leadership')) || [
        { name: "Tashpulatov Mirzo Ziyodovich", role: "Agentlik Direktori", hours: "Chorshanba 10:00 - 12:00", email: "garden@agro.uz" },
        { name: "Mirzayev Oybek Farxodovich", role: "Direktor Birinchi O'rinbosari", hours: "Payshanba 14:00 - 16:00", email: "garden@agro.uz" },
        { name: "Karimova Nigora Ravshanovna", role: "Direktor O'rinbosari", hours: "Juma 10:00 - 12:00", email: "garden@agro.uz" }
      ];

      saved.forEach((l, idx) => {
        const i = idx + 1;
        if (document.getElementById(`leader${i}_name`)) {
          document.getElementById(`leader${i}_name`).value = l.name;
          document.getElementById(`leader${i}_role`).value = l.role;
          document.getElementById(`leader${i}_hours`).value = l.hours;
          document.getElementById(`leader${i}_email`).value = l.email;
        }
      });

      document.getElementById('saveLeadershipBtn').addEventListener('click', () => {
        const updated = [
          {
            name: document.getElementById('leader1_name').value,
            role: document.getElementById('leader1_role').value,
            hours: document.getElementById('leader1_hours').value,
            email: document.getElementById('leader1_email').value
          },
          {
            name: document.getElementById('leader2_name').value,
            role: document.getElementById('leader2_role').value,
            hours: document.getElementById('leader2_hours').value,
            email: document.getElementById('leader2_email').value
          },
          {
            name: document.getElementById('leader3_name').value,
            role: document.getElementById('leader3_role').value,
            hours: document.getElementById('leader3_hours').value,
            email: document.getElementById('leader3_email').value
          }
        ];

        localStorage.setItem('agro_leadership', JSON.stringify(updated));
        alert("Markaziy rahbariyat ma'lumotlari saqlandi!");
      });
    }"""

new_js_leadership = """    function initLeadershipForm() {
      const container = document.getElementById('centralLeadershipForm');
      if(!container) return;

      const defaultLeadership = [
        { name: "Tashpulatov Mirzo Ziyodovich", role: "Agentlik Direktori", hours: "Chorshanba 10:00 - 12:00", email: "garden@agro.uz", desc: "Agentlik faoliyatiga umumiy rahbarlik qilish, davlat va xalqaro tashkilotlarda agentlik manfaatlarini ifodalash, subsidiyalar ajratilishini nazorat qilish." },
        { name: "Mirzayev Oybek Farxodovich", role: "Direktor Birinchi O'rinbosari", hours: "Payshanba 14:00 - 16:00", email: "garden@agro.uz", desc: "Resurs-tejamkor suv texnologiyalarini va intensiv bog'dorchilik loyihalarini o'rganish, monitoring va istiqbolli dasturlarni muvofiqlashtirish." },
        { name: "Karimova Nigora Ravshanovna", role: "Direktor O'rinbosari", hours: "Seshanba 09:00 - 11:00", email: "garden@agro.uz", desc: "Investitsiya dasturlari ijrosini ta'minlash, axborot-tahlil va raqamlashtirish jarayonlarini yuritish (REAGRO, Agrosubsidiya)." }
      ];

      const render = () => {
        let saved = JSON.parse(localStorage.getItem('agro_leadership')) || defaultLeadership;
        let html = '';
        saved.forEach((item, index) => {
          html += `
            <div style="background: var(--bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); border: 1px solid var(--border-color); position:relative;">
              <button class="btn delete-leader-btn" data-index="${index}" style="position:absolute; top: 10px; right: 10px; background: #ef4444; color: white; padding: 0.2rem 0.5rem; border: none; border-radius: 4px; cursor: pointer;"><i class="fas fa-trash"></i></button>
              <h4 style="font-size: 1rem; color: var(--primary-700); margin-bottom: 1rem;">${index + 1}. ${item.role}</h4>
              <div class="form-group"><label class="form-label">F.I.SH.</label><input type="text" class="form-input leader-input" data-index="${index}" data-field="name" value="${item.name}"></div>
              <div class="form-group"><label class="form-label">Lavozimi</label><input type="text" class="form-input leader-input" data-index="${index}" data-field="role" value="${item.role}"></div>
              <div class="form-group"><label class="form-label">Qabul Vaqti</label><input type="text" class="form-input leader-input" data-index="${index}" data-field="hours" value="${item.hours}"></div>
              <div class="form-group"><label class="form-label">Email</label><input type="email" class="form-input leader-input" data-index="${index}" data-field="email" value="${item.email}"></div>
            </div>`;
        });
        container.innerHTML = html;

        document.querySelectorAll('.delete-leader-btn').forEach(btn => {
          btn.addEventListener('click', (e) => {
            const idx = e.currentTarget.dataset.index;
            saved.splice(idx, 1);
            localStorage.setItem('agro_leadership', JSON.stringify(saved));
            render();
          });
        });
      };
      
      render();

      const saveBtn = document.getElementById('saveLeadershipBtn');
      if (saveBtn) {
        saveBtn.addEventListener('click', () => {
          let saved = JSON.parse(localStorage.getItem('agro_leadership')) || defaultLeadership;
          document.querySelectorAll('.leader-input').forEach(input => {
            const idx = input.dataset.index;
            const field = input.dataset.field;
            saved[idx][field] = input.value;
          });
          localStorage.setItem('agro_leadership', JSON.stringify(saved));
          alert("Markaziy rahbariyat ma'lumotlari saqlandi!");
        });
      }

      const addBtn = document.getElementById('addLeaderBtn');
      if (addBtn) {
        addBtn.addEventListener('click', () => {
          const name = document.getElementById('newLeaderName').value;
          const role = document.getElementById('newLeaderRole').value;
          const hours = document.getElementById('newLeaderHours').value;
          const email = document.getElementById('newLeaderEmail').value;
          const desc = document.getElementById('newLeaderDesc').value;
          if(!name || !role) { alert("Ism va Lavozim kiritilishi shart!"); return; }
          
          let saved = JSON.parse(localStorage.getItem('agro_leadership')) || defaultLeadership;
          saved.push({ name, role, hours, email, desc });
          localStorage.setItem('agro_leadership', JSON.stringify(saved));
          
          document.getElementById('newLeaderName').value = '';
          document.getElementById('newLeaderRole').value = '';
          document.getElementById('newLeaderHours').value = '';
          document.getElementById('newLeaderEmail').value = '';
          document.getElementById('newLeaderDesc').value = '';
          
          render();
          alert("Yangi rahbar qo'shildi!");
        });
      }
    }"""

content = content.replace(old_js_leadership, new_js_leadership)

# 4. Replace JS for Regions
old_js_regions = """    function initRegionalForm() {
      const container = document.getElementById('regionalDirectorsForm');
      const saved = JSON.parse(localStorage.getItem('agro_regions')) || defaultRegions;

      let html = '';
      Object.keys(saved).forEach(key => {
        const item = saved[key];
        html += `
          <div style="background: var(--bg-secondary); padding: 1.25rem; border-radius: var(--radius-md); border: 1px solid var(--border-color);">
            <h4 style="font-size: 0.95rem; color: var(--primary-700); margin-bottom: 0.75rem;">${item.name}</h4>
            <div class="form-group">
              <label class="form-label">Boshqarma Boshlig'i (F.I.SH.)</label>
              <input type="text" class="form-input region-head-input" data-key="${key}" value="${item.head}">
            </div>
            <div class="form-group">
              <label class="form-label">Telefon Raqami</label>
              <input type="text" class="form-input region-phone-input" data-key="${key}" value="${item.phone}">
            </div>
          </div>
        `;
      });
      container.innerHTML = html;

      document.getElementById('saveRegionsBtn').addEventListener('click', () => {
        const updated = { ...saved };
        document.querySelectorAll('.region-head-input').forEach(input => {
          const k = input.dataset.key;
          updated[k].head = input.value;
        });
        document.querySelectorAll('.region-phone-input').forEach(input => {
          const k = input.dataset.key;
          updated[k].phone = input.value;
        });

        localStorage.setItem('agro_regions', JSON.stringify(updated));
        alert("Hududiy boshqarma direktorlari muvaffaqiyatli saqlandi!");
      });
    }"""

new_js_regions = """    function initRegionalForm() {
      const container = document.getElementById('regionalDirectorsForm');
      if(!container) return;

      const render = () => {
        let saved = JSON.parse(localStorage.getItem('agro_regions')) || defaultRegions;
        let html = '';
        Object.keys(saved).forEach(key => {
          const item = saved[key];
          html += `
            <div style="background: var(--bg-secondary); padding: 1.25rem; border-radius: var(--radius-md); border: 1px solid var(--border-color); position: relative;">
              <button class="btn delete-region-btn" data-key="${key}" style="position:absolute; top: 10px; right: 10px; background: #ef4444; color: white; padding: 0.2rem 0.5rem; border: none; border-radius: 4px; cursor: pointer;"><i class="fas fa-trash"></i></button>
              <h4 style="font-size: 0.95rem; color: var(--primary-700); margin-bottom: 0.75rem;">${item.name}</h4>
              <div class="form-group">
                <label class="form-label">Boshqarma nomi</label>
                <input type="text" class="form-input region-input" data-key="${key}" data-field="name" value="${item.name}">
              </div>
              <div class="form-group">
                <label class="form-label">Boshqarma Boshlig'i (F.I.SH.)</label>
                <input type="text" class="form-input region-input" data-key="${key}" data-field="head" value="${item.head}">
              </div>
              <div class="form-group">
                <label class="form-label">Telefon Raqami</label>
                <input type="text" class="form-input region-input" data-key="${key}" data-field="phone" value="${item.phone}">
              </div>
            </div>`;
        });
        container.innerHTML = html;

        document.querySelectorAll('.delete-region-btn').forEach(btn => {
          btn.addEventListener('click', (e) => {
            const k = e.currentTarget.dataset.key;
            delete saved[k];
            localStorage.setItem('agro_regions', JSON.stringify(saved));
            render();
          });
        });
      };
      
      render();

      const saveBtn = document.getElementById('saveRegionsBtn');
      if (saveBtn) {
        saveBtn.onclick = () => {
          let saved = JSON.parse(localStorage.getItem('agro_regions')) || defaultRegions;
          document.querySelectorAll('.region-input').forEach(input => {
            const k = input.dataset.key;
            const field = input.dataset.field;
            if(saved[k]) saved[k][field] = input.value;
          });
          localStorage.setItem('agro_regions', JSON.stringify(saved));
          alert("Hududiy boshqarma direktorlari muvaffaqiyatli saqlandi!");
        };
      }

      const addBtn = document.getElementById('addRegionBtn');
      if (addBtn) {
        addBtn.onclick = () => {
          const id = document.getElementById('newRegionId').value.trim();
          const name = document.getElementById('newRegionName').value;
          const head = document.getElementById('newRegionHead').value;
          const phone = document.getElementById('newRegionPhone').value;
          if(!id || !name) { alert("ID va Boshqarma nomi kiritilishi shart!"); return; }
          
          let saved = JSON.parse(localStorage.getItem('agro_regions')) || defaultRegions;
          saved[id] = { name, head, phone };
          localStorage.setItem('agro_regions', JSON.stringify(saved));
          
          document.getElementById('newRegionId').value = '';
          document.getElementById('newRegionName').value = '';
          document.getElementById('newRegionHead').value = '';
          document.getElementById('newRegionPhone').value = '';
          
          render();
          alert("Yangi hudud qo'shildi!");
        };
      }
    }"""
    
content = content.replace(old_js_regions, new_js_regions)

with open("admin.html", "w", encoding="utf-8") as f:
    f.write(content)

print("admin.html has been updated successfully via string replacement.")

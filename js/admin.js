"use strict";

const adminState = {
  content: { leadership: [], regions: {}, news: [] },
  contacts: [],
  editingNewsId: null,
  language: "uz",
  newsDraft: null
};

const adminLanguages = {
  uz: { label: "O‘zbekcha", short: "O‘Z" },
  ru: { label: "Русский", short: "РУ" },
  en: { label: "English", short: "EN" }
};

const newsLocalizedFields = ["title", "category", "author", "excerpt", "content"];
const adminEmailPattern = /^[A-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?(?:\.[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?)+$/i;
const adminNamePattern = /^[\p{L}\s.'‘’ʻʼ`-]+$/u;

function checkedText(value, label, { minimum = 0, maximum = 1200 } = {}) {
  const text = String(value ?? "").trim();
  if (text.length < minimum) throw new Error(`${label} kamida ${minimum} ta belgidan iborat bo‘lishi kerak.`);
  if (text.length > maximum) throw new Error(`${label} ${maximum} ta belgidan oshmasligi kerak.`);
  if (/[<>]/.test(text) || /[\u0000-\u0008\u000B\u000C\u000E-\u001F]/.test(text)) {
    throw new Error(`${label} tarkibida ruxsat etilmagan belgi bor.`);
  }
  return text;
}

function checkedName(value, label) {
  const text = checkedText(value, label, { minimum: 2, maximum: 160 });
  if (!adminNamePattern.test(text) || (text.match(/\p{L}/gu) || []).length < 2) {
    throw new Error(`${label} faqat harflar va ismga xos belgilar bilan to‘liq kiritilishi kerak.`);
  }
  return text;
}

function checkedEmail(value, label = "Email") {
  const text = checkedText(value, label, { maximum: 160 });
  if (text && !adminEmailPattern.test(text)) throw new Error(`${label} formati noto‘g‘ri. Masalan: name@example.uz`);
  return text;
}

function checkedPhone(value, label = "Telefon") {
  const text = checkedText(value, label, { maximum: 40 });
  if (!text) return text;
  const digits = text.replace(/\D/g, "");
  if (!/^\+?[0-9()\-\s]+$/.test(text) || digits.length !== 12 || !digits.startsWith("998")) {
    throw new Error(`${label} +998 XX XXX-XX-XX formatida bo‘lishi kerak.`);
  }
  return text;
}

function checkedDate(value) {
  const text = checkedText(value, "Sana", { minimum: 10, maximum: 10 });
  if (!/^\d{4}-\d{2}-\d{2}$/.test(text)) throw new Error("Sana YYYY-MM-DD formatida bo‘lishi kerak.");
  const parsed = new Date(`${text}T00:00:00Z`);
  if (Number.isNaN(parsed.getTime()) || parsed.toISOString().slice(0, 10) !== text) throw new Error("Haqiqiy sana kiriting.");
  const maximum = new Date();
  maximum.setUTCFullYear(maximum.getUTCFullYear() + 1);
  if (text < "2000-01-01" || parsed > maximum) throw new Error("Sana ruxsat etilgan davrdan tashqarida.");
  return text;
}

function validateTranslation(record, language, fields, label) {
  const values = record.translations?.[language] || {};
  const hasAny = fields.some(([field]) => String(values[field] || "").trim());
  fields.forEach(([field, minimum, maximum]) => {
    values[field] = checkedText(values[field] || "", `${label} — ${adminLanguages[language].label} ${field}`, {
      minimum: hasAny ? minimum : 0,
      maximum
    });
  });
}

function validateLeadershipDraft() {
  if (!adminState.content.leadership.length || adminState.content.leadership.length > 50) throw new Error("Rahbariyat ro‘yxati 1–50 ta yozuvdan iborat bo‘lishi kerak.");
  adminState.content.leadership.forEach((person, index) => {
    const prefix = `${index + 1}-rahbar`;
    person.name = checkedName(person.name, `${prefix} F.I.SH.`);
    person.role = checkedText(person.role, `${prefix} lavozimi`, { minimum: 2, maximum: 180 });
    person.hours = checkedText(person.hours, `${prefix} qabul vaqti`, { maximum: 120 });
    person.email = checkedEmail(person.email, `${prefix} emaili`);
    person.desc = checkedText(person.desc, `${prefix} vakolatlari`, { maximum: 1200 });
    ["ru", "en"].forEach(language => validateTranslation(person, language, [["name", 2, 160], ["role", 2, 180], ["hours", 0, 120], ["desc", 0, 1200]], prefix));
  });
}

function validateRegionsDraft() {
  const entries = Object.entries(adminState.content.regions);
  if (!entries.length || entries.length > 50) throw new Error("Hududlar ro‘yxati 1–50 ta yozuvdan iborat bo‘lishi kerak.");
  entries.forEach(([key, region]) => {
    if (!/^[a-z0-9_-]{2,50}$/.test(key)) throw new Error(`${key} hudud ID-si noto‘g‘ri.`);
    region.name = checkedText(region.name, `${key} boshqarma nomi`, { minimum: 2, maximum: 180 });
    region.head = checkedText(region.head, `${key} rahbari`, { maximum: 160 });
    region.phone = checkedPhone(region.phone, `${key} telefoni`);
    region.address = checkedText(region.address, `${key} manzili`, { maximum: 300 });
    region.projects = checkedText(region.projects, `${key} loyihalari`, { maximum: 1200 });
    ["ru", "en"].forEach(language => validateTranslation(region, language, [["name", 2, 180], ["head", 0, 160], ["address", 0, 300], ["projects", 0, 1200]], key));
  });
}

function validateNewsDraft() {
  const required = { title: [4, 240], category: [2, 80], author: [0, 160], excerpt: [10, 1200], content: [20, 20000] };
  Object.entries(required).forEach(([field, [minimum, maximum]]) => {
    adminState.newsDraft.uz[field] = checkedText(adminState.newsDraft.uz[field], `O‘zbekcha ${field}`, { minimum, maximum });
  });
  ["ru", "en"].forEach(language => {
    const values = adminState.newsDraft[language];
    const hasAny = Object.keys(required).some(field => String(values[field] || "").trim());
    Object.entries(required).forEach(([field, [minimum, maximum]]) => {
      values[field] = checkedText(values[field] || "", `${adminLanguages[language].label} ${field}`, { minimum: hasAny ? minimum : 0, maximum });
    });
  });
  return checkedDate(document.getElementById("newsDateInput").value);
}

function createNewsDraft(article = {}) {
  const draft = {};
  Object.keys(adminLanguages).forEach(language => {
    draft[language] = {};
    newsLocalizedFields.forEach(field => {
      draft[language][field] = language === "uz"
        ? (article[field] || (field === "author" ? "Agentlik Matbuot Xizmati" : ""))
        : (article.translations?.[language]?.[field] || "");
    });
  });
  return draft;
}

function localizedAdminValue(record, field, language = adminState.language) {
  if (language === "uz") return record[field] || "";
  return record.translations?.[language]?.[field] || "";
}

function setLocalizedAdminValue(record, field, value, language = adminState.language) {
  if (language === "uz") {
    record[field] = value;
    return;
  }
  record.translations ||= {};
  record.translations[language] ||= {};
  record.translations[language][field] = value;
}

document.addEventListener("DOMContentLoaded", () => {
  adminState.newsDraft = createNewsDraft();
  bindAdminEvents();
  checkAdminSession();
});

function adminElement(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function adminIcon(className) {
  const node = document.createElement("i");
  node.className = className;
  node.setAttribute("aria-hidden", "true");
  return node;
}

async function adminApi(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: {
      Accept: "application/json",
      ...(options.body ? { "Content-Type": "application/json" } : {}),
      ...(options.headers || {})
    },
    cache: "no-store"
  });
  const result = await response.json().catch(() => ({}));
  if (!response.ok) {
    const error = new Error(result.error || `Server xatosi (${response.status})`);
    error.status = response.status;
    throw error;
  }
  return result;
}

function bindAdminEvents() {
  document.getElementById("adminLoginForm").addEventListener("submit", handleLogin);
  document.getElementById("adminLogoutButton").addEventListener("click", handleLogout);
  document.querySelectorAll("[data-admin-section]").forEach(button => {
    button.addEventListener("click", () => openAdminSection(button.dataset.adminSection));
  });
  document.getElementById("addLeaderButton").addEventListener("click", addLeader);
  document.getElementById("saveLeadershipButton").addEventListener("click", saveLeadership);
  document.getElementById("addRegionForm").addEventListener("submit", addRegion);
  document.getElementById("saveRegionsButton").addEventListener("click", saveRegions);
  document.getElementById("adminNewsForm").addEventListener("submit", saveNews);
  document.getElementById("cancelNewsEditButton").addEventListener("click", resetNewsForm);
  document.getElementById("refreshContactsButton").addEventListener("click", loadContacts);
  document.querySelectorAll("[data-admin-language]").forEach(button => {
    button.addEventListener("click", () => setAdminLanguage(button.dataset.adminLanguage));
  });
  document.querySelectorAll("[data-admin-goto]").forEach(button => {
    button.addEventListener("click", () => openAdminSection(button.dataset.adminGoto));
  });
}

function setAdminLanguage(language) {
  if (!adminLanguages[language] || language === adminState.language) return;
  adminState.language = language;
  document.querySelectorAll("[data-admin-language]").forEach(button => {
    const active = button.dataset.adminLanguage === language;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  });
  renderLeadershipEditor();
  renderRegionsEditor();
  renderNewsLanguageEditor();
  renderNewsList();
}

async function checkAdminSession() {
  const status = document.getElementById("adminLoginStatus");
  try {
    const session = await adminApi("/api/admin/session");
    document.getElementById("adminSetupNote").hidden = session.configured;
    if (session.authenticated) {
      await showAdminApp();
    }
  } catch (error) {
    status.className = "status-message status-error";
    status.textContent = "Server bilan bog‘lanib bo‘lmadi. Loyihani server.py orqali ishga tushiring.";
  }
}

async function handleLogin(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const submit = form.querySelector("button[type='submit']");
  const status = document.getElementById("adminLoginStatus");
  submit.disabled = true;
  status.className = "status-message";
  status.textContent = "Tekshirilmoqda…";
  try {
    await adminApi("/api/admin/login", {
      method: "POST",
      body: JSON.stringify({
        username: form.elements.username.value,
        password: form.elements.password.value
      })
    });
    form.reset();
    status.textContent = "";
    await showAdminApp();
  } catch (error) {
    status.className = "status-message status-error";
    status.textContent = error.message;
  } finally {
    submit.disabled = false;
  }
}

async function handleLogout() {
  try {
    await adminApi("/api/admin/logout", { method: "POST", body: "{}" });
  } finally {
    adminState.content = { leadership: [], regions: {}, news: [] };
    adminState.contacts = [];
    document.getElementById("adminApp").hidden = true;
    document.getElementById("adminLoginView").hidden = false;
  }
}

async function showAdminApp() {
  document.getElementById("adminLoginView").hidden = true;
  document.getElementById("adminApp").hidden = false;
  try {
    const [content, contactsResult] = await Promise.all([
      adminApi("/api/content"),
      adminApi("/api/admin/contacts")
    ]);
    adminState.content = {
      leadership: Array.isArray(content.leadership) ? content.leadership : [],
      regions: content.regions && typeof content.regions === "object" ? content.regions : {},
      news: Array.isArray(content.news) ? content.news : []
    };
    adminState.newsDraft = createNewsDraft();
    adminState.contacts = contactsResult.contacts || [];
    renderAllAdminContent();
  } catch (error) {
    if (error.status === 401) {
      await handleLogout();
      return;
    }
    showToast(error.message, true);
  }
}

function openAdminSection(section) {
  const titles = {
    dashboard: "Boshqaruv paneli",
    leadership: "Rahbariyat",
    regions: "Hududiy boshqarmalar",
    news: "Yangiliklar",
    contacts: "Murojaatlar"
  };
  document.querySelectorAll("[data-admin-section]").forEach(button => {
    button.classList.toggle("active", button.dataset.adminSection === section);
  });
  document.querySelectorAll("[data-section-panel]").forEach(panel => {
    panel.classList.toggle("active", panel.dataset.sectionPanel === section);
  });
  document.getElementById("adminPageTitle").textContent = titles[section] || "Admin panel";
  const breadcrumb = document.getElementById("adminBreadcrumb");
  if (breadcrumb) breadcrumb.textContent = titles[section] || "Admin panel";
}

function renderAllAdminContent() {
  renderDashboard();
  renderLeadershipEditor();
  renderRegionsEditor();
  renderNewsList();
  renderNewsLanguageEditor();
  renderContacts();
}

function renderDashboard() {
  document.getElementById("dashboardLeadershipCount").textContent = adminState.content.leadership.length;
  document.getElementById("dashboardRegionCount").textContent = Object.keys(adminState.content.regions).length;
  document.getElementById("dashboardNewsCount").textContent = adminState.content.news.length;
  document.getElementById("dashboardContactCount").textContent = adminState.contacts.length;
  const translationGroups = [
    ...adminState.content.leadership.map(item => [item, ["name", "role", "desc"]]),
    ...Object.values(adminState.content.regions).map(item => [item, ["name", "address", "projects"]]),
    ...adminState.content.news.map(item => [item, ["title", "excerpt", "content"]])
  ];
  let total = 0;
  let completed = 0;
  translationGroups.forEach(([record, fields]) => {
    ["ru", "en"].forEach(language => {
      fields.forEach(field => {
        total += 1;
        if (String(record.translations?.[language]?.[field] || "").trim()) completed += 1;
      });
    });
  });
  const percent = total ? Math.round((completed / total) * 100) : 0;
  const percentNode = document.getElementById("dashboardTranslationPercent");
  const progressNode = document.getElementById("dashboardTranslationBar");
  const summaryNode = document.getElementById("dashboardTranslationSummary");
  if (percentNode) percentNode.textContent = `${percent}%`;
  if (progressNode) progressNode.style.width = `${percent}%`;
  if (summaryNode) summaryNode.textContent = `${completed} / ${total}`;
  const now = new Date();
  const time = new Intl.DateTimeFormat("uz-UZ", { hour: "2-digit", minute: "2-digit", hour12: false }).format(now);
  const liveTime = document.getElementById("dashboardLiveTime");
  const lastSync = document.getElementById("dashboardLastSync");
  if (liveTime) liveTime.textContent = time;
  if (lastSync) lastSync.textContent = time;
}

function labeledInput(labelText, value, onInput, options = {}) {
  const group = adminElement("div", "form-group");
  const label = adminElement("label", "form-label", labelText);
  const input = options.multiline ? adminElement("textarea", "form-input") : adminElement("input", "form-input");
  if (options.multiline) input.rows = options.rows || 3;
  else input.type = options.type || "text";
  input.value = value || "";
  input.maxLength = options.maxLength || 1200;
  if (options.minLength) input.minLength = options.minLength;
  input.required = Boolean(options.required);
  if (options.inputMode) input.inputMode = options.inputMode;
  if (options.autocomplete) input.autocomplete = options.autocomplete;
  if (options.placeholder) input.placeholder = options.placeholder;
  input.addEventListener("input", () => {
    input.setCustomValidity("");
    input.classList.remove("is-invalid");
    onInput(input.value);
  });
  if (options.validate) {
    input.addEventListener("blur", () => {
      try {
        options.validate(input.value);
        input.setCustomValidity("");
        input.classList.remove("is-invalid");
      } catch (error) {
        input.setCustomValidity(error.message);
        input.classList.add("is-invalid");
      }
    });
  }
  group.append(label, input);
  return group;
}

function renderLeadershipEditor() {
  const container = document.getElementById("leadershipEditor");
  container.replaceChildren();
  adminState.content.leadership.forEach((person, index) => {
    const card = adminElement("article", "admin-card admin-editor-card");
    const header = adminElement("div", "admin-editor-header");
    const currentName = localizedAdminValue(person, "name") || person.name || "Yangi rahbar";
    const heading = adminElement("div");
    heading.append(
      adminElement("span", "admin-editor-language-badge", adminLanguages[adminState.language].label),
      adminElement("h3", "", `${index + 1}. ${currentName}`)
    );
    header.append(heading);
    const remove = adminElement("button", "admin-icon-button danger");
    remove.type = "button";
    remove.title = "O‘chirish";
    remove.setAttribute("aria-label", `${person.name || "Rahbar"}ni o‘chirish`);
    remove.append(adminIcon("fas fa-trash"));
    remove.addEventListener("click", () => {
      if (!window.confirm("Ushbu rahbarni ro‘yxatdan olib tashlaysizmi? O‘zgarish Saqlash tugmasidan keyin kuchga kiradi.")) return;
      adminState.content.leadership.splice(index, 1);
      renderLeadershipEditor();
      renderDashboard();
    });
    header.append(remove);
    const grid = adminElement("div", "admin-form-grid");
    grid.append(
      labeledInput("F.I.SH.", localizedAdminValue(person, "name"), value => setLocalizedAdminValue(person, "name", value), { required: adminState.language === "uz", maxLength: 160, validate: value => { if (adminState.language === "uz" || value.trim()) checkedName(value, "F.I.SH."); } }),
      labeledInput("Lavozim", localizedAdminValue(person, "role"), value => setLocalizedAdminValue(person, "role", value), { required: adminState.language === "uz" }),
      labeledInput("Qabul vaqti", localizedAdminValue(person, "hours"), value => setLocalizedAdminValue(person, "hours", value)),
      labeledInput("Email", person.email, value => { person.email = value; }, { type: "email", maxLength: 160, inputMode: "email", autocomplete: "email", validate: value => checkedEmail(value) })
    );
    const description = labeledInput("Vakolatlari", localizedAdminValue(person, "desc"), value => setLocalizedAdminValue(person, "desc", value), { multiline: true, rows: 3 });
    description.classList.add("admin-span-2");
    const photoField = adminElement("div", "form-group admin-span-2 leader-photo-editor");
    photoField.append(adminElement("label", "form-label", "Rahbar rasmi (PNG, JPEG yoki WEBP — 2 MB gacha)"));
    const photoRow = adminElement("div", "leader-photo-editor-row");
    const preview = adminElement("div", "leader-photo-preview");
    if (person.photo) {
      const previewImage = document.createElement("img");
      previewImage.src = person.photo;
      previewImage.alt = `${person.name || "Rahbar"} rasmi`;
      preview.append(previewImage);
    } else {
      preview.append(adminIcon("fas fa-user"), adminElement("span", "", "Rasm yuklanmagan"));
    }
    const photoActions = adminElement("div", "leader-photo-editor-actions");
    const photoInput = adminElement("input", "form-input");
    photoInput.type = "file";
    photoInput.accept = "image/png,image/jpeg,image/webp";
    photoInput.addEventListener("change", async () => {
      const file = photoInput.files[0];
      if (!file) return;
      try {
        person.photo = await readImage(file);
        renderLeadershipEditor();
        showToast("Rahbar rasmi tayyorlandi. O‘zgarishni saqlashni unutmang.");
      } catch (error) {
        photoInput.value = "";
        showToast(error.message, true);
      }
    });
    photoActions.append(photoInput);
    if (person.photo) {
      const removePhoto = adminElement("button", "btn btn-outline leader-photo-remove", "Rasmni olib tashlash");
      removePhoto.type = "button";
      removePhoto.addEventListener("click", () => {
        person.photo = "";
        renderLeadershipEditor();
      });
      photoActions.append(removePhoto);
    }
    photoRow.append(preview, photoActions);
    photoField.append(photoRow);
    grid.append(description, photoField);
    card.append(header, grid);
    container.append(card);
  });
}

function addLeader() {
  adminState.content.leadership.push({
    name: "Yangi rahbar",
    role: "Lavozim",
    hours: "",
    email: "",
    desc: "",
    photo: "",
    translations: { ru: {}, en: {} }
  });
  renderLeadershipEditor();
  renderDashboard();
  document.getElementById("leadershipEditor").lastElementChild?.scrollIntoView({ behavior: "smooth", block: "center" });
}

async function saveLeadership() {
  try {
    validateLeadershipDraft();
    await adminApi("/api/admin/leadership", {
      method: "PUT",
      body: JSON.stringify(adminState.content.leadership)
    });
    showToast("Ma’lumotlar tekshirildi va rahbariyat saqlandi.");
  } catch (error) {
    showToast(error.message, true);
  }
}

function renderRegionsEditor() {
  const container = document.getElementById("regionsEditor");
  container.replaceChildren();
  Object.entries(adminState.content.regions).forEach(([key, region]) => {
    const card = adminElement("article", "admin-card admin-editor-card");
    const header = adminElement("div", "admin-editor-header");
    const titleBlock = adminElement("div");
    titleBlock.append(
      adminElement("p", "admin-eyebrow", `${key} · ${adminLanguages[adminState.language].label}`),
      adminElement("h3", "", localizedAdminValue(region, "name") || region.name)
    );
    const remove = adminElement("button", "admin-icon-button danger");
    remove.type = "button";
    remove.title = "O‘chirish";
    remove.setAttribute("aria-label", `${region.name}ni o‘chirish`);
    remove.append(adminIcon("fas fa-trash"));
    remove.addEventListener("click", () => {
      if (!window.confirm(`${region.name} ro‘yxatdan o‘chirilsinmi? O‘zgarish Saqlash tugmasidan keyin kuchga kiradi.`)) return;
      delete adminState.content.regions[key];
      renderRegionsEditor();
      renderDashboard();
    });
    header.append(titleBlock, remove);
    const grid = adminElement("div", "admin-form-grid");
    grid.append(
      labeledInput("Boshqarma nomi", localizedAdminValue(region, "name"), value => setLocalizedAdminValue(region, "name", value), { required: adminState.language === "uz" }),
      labeledInput("Rahbar", localizedAdminValue(region, "head"), value => setLocalizedAdminValue(region, "head", value)),
      labeledInput("Telefon", region.phone, value => { region.phone = value; }, { type: "tel", maxLength: 40, inputMode: "tel", placeholder: "+998 XX XXX-XX-XX", validate: value => checkedPhone(value) }),
      labeledInput("Manzil", localizedAdminValue(region, "address"), value => setLocalizedAdminValue(region, "address", value))
    );
    const projects = labeledInput("Asosiy loyihalar", localizedAdminValue(region, "projects"), value => setLocalizedAdminValue(region, "projects", value), { multiline: true, rows: 3 });
    projects.classList.add("admin-span-2");
    grid.append(projects);
    card.append(header, grid);
    container.append(card);
  });
}

function addRegion(event) {
  event.preventDefault();
  const idInput = document.getElementById("newRegionId");
  const nameInput = document.getElementById("newRegionName");
  const id = idInput.value.trim();
  let name;
  try {
    if (!/^[a-z0-9_-]{2,50}$/.test(id)) throw new Error("Hudud ID-si 2–50 ta kichik lotin harfi, raqam, _ yoki - dan iborat bo‘lishi kerak.");
    name = checkedText(nameInput.value, "Boshqarma nomi", { minimum: 2, maximum: 180 });
  } catch (error) {
    showToast(error.message, true);
    return;
  }
  if (adminState.content.regions[id]) {
    showToast("Bu ID bilan hudud mavjud.", true);
    return;
  }
  adminState.content.regions[id] = { name, head: "", phone: "", address: "", projects: "", translations: { ru: {}, en: {} } };
  event.currentTarget.reset();
  renderRegionsEditor();
  renderDashboard();
}

async function saveRegions() {
  try {
    validateRegionsDraft();
    await adminApi("/api/admin/regions", {
      method: "PUT",
      body: JSON.stringify(adminState.content.regions)
    });
    showToast("Ma’lumotlar tekshirildi va hududiy boshqarmalar saqlandi.");
  } catch (error) {
    showToast(error.message, true);
  }
}

function renderNewsList() {
  const container = document.getElementById("adminNewsList");
  container.replaceChildren();
  adminState.content.news.forEach(article => {
    const card = adminElement("article", "admin-card admin-news-row");
    const image = adminElement("img", "admin-news-thumb");
    image.src = article.image || "assets/hero_agri.jpg";
    image.alt = "";
    const body = adminElement("div", "admin-news-row-body");
    body.append(
      adminElement("p", "admin-eyebrow", `${article.date} · ${localizedAdminValue(article, "category") || article.category}`),
      adminElement("h3", "", localizedAdminValue(article, "title") || article.title),
      adminElement("p", "", localizedAdminValue(article, "excerpt") || article.excerpt)
    );
    const actions = adminElement("div", "admin-row-actions");
    const edit = adminElement("button", "btn btn-secondary", "Tahrirlash");
    edit.type = "button";
    edit.addEventListener("click", () => editNews(article));
    const remove = adminElement("button", "btn admin-danger-button", "O‘chirish");
    remove.type = "button";
    remove.addEventListener("click", () => deleteNews(article));
    actions.append(edit, remove);
    card.append(image, body, actions);
    container.append(card);
  });
}

function editNews(article) {
  adminState.editingNewsId = Number(article.id);
  document.getElementById("newsFormTitle").textContent = "Xabarni tahrirlash";
  document.getElementById("newsSubmitLabel").textContent = "Saqlash";
  document.getElementById("cancelNewsEditButton").hidden = false;
  adminState.newsDraft = createNewsDraft(article);
  document.getElementById("newsDateInput").value = article.date;
  renderNewsLanguageEditor();
  document.getElementById("adminNewsForm").scrollIntoView({ behavior: "smooth", block: "start" });
}

function renderNewsLanguageEditor() {
  const container = document.getElementById("newsLocalizedFields");
  if (!container) return;
  adminState.newsDraft ||= createNewsDraft();
  const language = adminState.language;
  const values = adminState.newsDraft[language];
  const required = language === "uz";
  container.replaceChildren();
  const notice = adminElement("div", "admin-language-notice");
  notice.append(
    adminIcon("fas fa-language"),
    adminElement("strong", "", `${adminLanguages[language].label} kontenti`),
    adminElement("span", "", required ? "Asosiy til — barcha majburiy maydonlarni kiriting." : "Bo‘sh qoldirilsa O‘zbekcha matn ko‘rsatiladi.")
  );
  const grid = adminElement("div", "admin-form-grid admin-localized-grid");
  const title = labeledInput("Sarlavha", values.title, value => { values.title = value; }, { maxLength: 240, required });
  title.classList.add("admin-span-2");
  const category = labeledInput("Kategoriya", values.category, value => { values.category = value; }, { maxLength: 80, required, placeholder: language === "uz" ? "Masalan: Rasmiy" : "Translated category" });
  const author = labeledInput("Muallif", values.author, value => { values.author = value; }, { maxLength: 160 });
  const excerpt = labeledInput("Qisqacha mazmun", values.excerpt, value => { values.excerpt = value; }, { multiline: true, rows: 3, maxLength: 1200, required });
  excerpt.classList.add("admin-span-2");
  const content = labeledInput("Batafsil matn", values.content, value => { values.content = value; }, { multiline: true, rows: 9, maxLength: 20000, required, placeholder: "Har bir xatboshini bo‘sh qator bilan ajrating." });
  content.classList.add("admin-span-2");
  grid.append(title, category, author, excerpt, content);
  container.append(notice, grid);
}

async function saveNews(event) {
  event.preventDefault();
  const submit = event.currentTarget.querySelector("button[type='submit']");
  submit.disabled = true;
  try {
    const validDate = validateNewsDraft();
    const existing = adminState.content.news.find(item => Number(item.id) === adminState.editingNewsId);
    const file = document.getElementById("newsImageInput").files[0];
    const image = file ? await readImage(file) : (existing?.image || "assets/hero_agri.jpg");
    const uz = adminState.newsDraft.uz;
    const article = {
      title: uz.title,
      category: uz.category,
      date: validDate,
      author: uz.author,
      image,
      excerpt: uz.excerpt,
      content: uz.content,
      translations: {
        ru: { ...adminState.newsDraft.ru },
        en: { ...adminState.newsDraft.en }
      }
    };
    if (adminState.editingNewsId) {
      await adminApi(`/api/admin/news/${adminState.editingNewsId}`, {
        method: "PUT",
        body: JSON.stringify(article)
      });
      Object.assign(existing, article);
      showToast("Ma’lumotlar tekshirildi va yangilik yangilandi.");
    } else {
      const result = await adminApi("/api/admin/news", {
        method: "POST",
        body: JSON.stringify(article)
      });
      adminState.content.news.unshift(result.article);
      showToast("Ma’lumotlar tekshirildi va yangi xabar nashr qilindi.");
    }
    resetNewsForm();
    renderNewsList();
    renderDashboard();
  } catch (error) {
    showToast(error.message, true);
  } finally {
    submit.disabled = false;
  }
}

async function deleteNews(article) {
  if (!window.confirm(`“${article.title}” yangiligini butunlay o‘chirasizmi?`)) return;
  try {
    await adminApi(`/api/admin/news/${article.id}`, { method: "DELETE" });
    adminState.content.news = adminState.content.news.filter(item => Number(item.id) !== Number(article.id));
    renderNewsList();
    renderDashboard();
    showToast("Yangilik o‘chirildi.");
  } catch (error) {
    showToast(error.message, true);
  }
}

function resetNewsForm() {
  adminState.editingNewsId = null;
  document.getElementById("adminNewsForm").reset();
  adminState.newsDraft = createNewsDraft();
  document.getElementById("newsDateInput").value = new Date().toISOString().slice(0, 10);
  renderNewsLanguageEditor();
  document.getElementById("newsFormTitle").textContent = "Yangi xabar joylash";
  document.getElementById("newsSubmitLabel").textContent = "Nashr qilish";
  document.getElementById("cancelNewsEditButton").hidden = true;
}

function readImage(file) {
  if (file.size > 2 * 1024 * 1024) return Promise.reject(new Error("Rasm hajmi 2 MB dan oshmasligi kerak."));
  if (!["image/png", "image/jpeg", "image/webp"].includes(file.type)) {
    return Promise.reject(new Error("Faqat PNG, JPEG yoki WEBP rasm yuklash mumkin."));
  }
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = () => reject(new Error("Rasmni o‘qib bo‘lmadi."));
    reader.readAsDataURL(file);
  });
}

async function loadContacts() {
  try {
    const result = await adminApi("/api/admin/contacts");
    adminState.contacts = result.contacts || [];
    renderContacts();
    renderDashboard();
    showToast("Murojaatlar yangilandi.");
  } catch (error) {
    showToast(error.message, true);
  }
}

function renderContacts() {
  const container = document.getElementById("contactsList");
  container.replaceChildren();
  if (!adminState.contacts.length) {
    container.append(adminElement("p", "status-message", "Hozircha murojaatlar yo‘q."));
    return;
  }
  adminState.contacts.forEach(contact => {
    const card = adminElement("article", "admin-card admin-contact-card");
    const header = adminElement("div", "admin-editor-header");
    header.append(
      adminElement("div", "", contact.name),
      adminElement("time", "admin-contact-time", new Date(contact.createdAt).toLocaleString("uz-UZ"))
    );
    card.append(
      header,
      adminElement("p", "admin-contact-address", contact.contact),
      adminElement("p", "admin-contact-message", contact.message),
      adminElement("code", "admin-reference", contact.id)
    );
    container.append(card);
  });
}

function showToast(message, isError = false) {
  const toast = document.getElementById("adminToast");
  toast.textContent = message;
  toast.className = `admin-toast visible${isError ? " error" : ""}`;
  window.clearTimeout(showToast.timeout);
  showToast.timeout = window.setTimeout(() => {
    toast.classList.remove("visible");
  }, 4000);
}

document.getElementById("newsDateInput").value = new Date().toISOString().slice(0, 10);

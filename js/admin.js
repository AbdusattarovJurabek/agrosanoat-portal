"use strict";

const adminState = {
  content: { leadership: [], regions: {}, news: [] },
  contacts: [],
  editingNewsId: null
};

document.addEventListener("DOMContentLoaded", () => {
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
}

function renderAllAdminContent() {
  renderDashboard();
  renderLeadershipEditor();
  renderRegionsEditor();
  renderNewsList();
  renderContacts();
}

function renderDashboard() {
  document.getElementById("dashboardLeadershipCount").textContent = adminState.content.leadership.length;
  document.getElementById("dashboardRegionCount").textContent = Object.keys(adminState.content.regions).length;
  document.getElementById("dashboardNewsCount").textContent = adminState.content.news.length;
  document.getElementById("dashboardContactCount").textContent = adminState.contacts.length;
}

function labeledInput(labelText, value, onInput, options = {}) {
  const group = adminElement("div", "form-group");
  const label = adminElement("label", "form-label", labelText);
  const input = options.multiline ? adminElement("textarea", "form-input") : adminElement("input", "form-input");
  if (options.multiline) input.rows = options.rows || 3;
  else input.type = options.type || "text";
  input.value = value || "";
  input.maxLength = options.maxLength || 1200;
  input.addEventListener("input", () => onInput(input.value));
  group.append(label, input);
  return group;
}

function renderLeadershipEditor() {
  const container = document.getElementById("leadershipEditor");
  container.replaceChildren();
  adminState.content.leadership.forEach((person, index) => {
    const card = adminElement("article", "admin-card admin-editor-card");
    const header = adminElement("div", "admin-editor-header");
    header.append(adminElement("h3", "", `${index + 1}. ${person.name || "Yangi rahbar"}`));
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
      labeledInput("F.I.SH.", person.name, value => { person.name = value; }),
      labeledInput("Lavozim", person.role, value => { person.role = value; }),
      labeledInput("Qabul vaqti", person.hours, value => { person.hours = value; }),
      labeledInput("Email", person.email, value => { person.email = value; }, { type: "email" })
    );
    const description = labeledInput("Vakolatlari", person.desc, value => { person.desc = value; }, { multiline: true, rows: 3 });
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
    photo: ""
  });
  renderLeadershipEditor();
  renderDashboard();
  document.getElementById("leadershipEditor").lastElementChild?.scrollIntoView({ behavior: "smooth", block: "center" });
}

async function saveLeadership() {
  try {
    await adminApi("/api/admin/leadership", {
      method: "PUT",
      body: JSON.stringify(adminState.content.leadership)
    });
    showToast("Rahbariyat ma’lumotlari saqlandi.");
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
    titleBlock.append(adminElement("p", "admin-eyebrow", key), adminElement("h3", "", region.name));
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
      labeledInput("Boshqarma nomi", region.name, value => { region.name = value; }),
      labeledInput("Rahbar", region.head, value => { region.head = value; }),
      labeledInput("Telefon", region.phone, value => { region.phone = value; }),
      labeledInput("Manzil", region.address, value => { region.address = value; })
    );
    const projects = labeledInput("Asosiy loyihalar", region.projects, value => { region.projects = value; }, { multiline: true, rows: 3 });
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
  const name = nameInput.value.trim();
  if (adminState.content.regions[id]) {
    showToast("Bu ID bilan hudud mavjud.", true);
    return;
  }
  adminState.content.regions[id] = { name, head: "", phone: "", address: "", projects: "" };
  event.currentTarget.reset();
  renderRegionsEditor();
  renderDashboard();
}

async function saveRegions() {
  try {
    await adminApi("/api/admin/regions", {
      method: "PUT",
      body: JSON.stringify(adminState.content.regions)
    });
    showToast("Hududiy boshqarmalar saqlandi.");
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
      adminElement("p", "admin-eyebrow", `${article.date} · ${article.category}`),
      adminElement("h3", "", article.title),
      adminElement("p", "", article.excerpt)
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
  document.getElementById("newsTitleInput").value = article.title;
  document.getElementById("newsCategoryInput").value = article.category;
  document.getElementById("newsDateInput").value = article.date;
  document.getElementById("newsAuthorInput").value = article.author || "Agentlik Matbuot Xizmati";
  document.getElementById("newsExcerptInput").value = article.excerpt;
  document.getElementById("newsContentInput").value = article.content;
  document.getElementById("adminNewsForm").scrollIntoView({ behavior: "smooth", block: "start" });
}

async function saveNews(event) {
  event.preventDefault();
  const submit = event.currentTarget.querySelector("button[type='submit']");
  submit.disabled = true;
  try {
    const existing = adminState.content.news.find(item => Number(item.id) === adminState.editingNewsId);
    const file = document.getElementById("newsImageInput").files[0];
    const image = file ? await readImage(file) : (existing?.image || "assets/hero_agri.jpg");
    const article = {
      title: document.getElementById("newsTitleInput").value,
      category: document.getElementById("newsCategoryInput").value,
      date: document.getElementById("newsDateInput").value,
      author: document.getElementById("newsAuthorInput").value,
      image,
      excerpt: document.getElementById("newsExcerptInput").value,
      content: document.getElementById("newsContentInput").value
    };
    if (adminState.editingNewsId) {
      await adminApi(`/api/admin/news/${adminState.editingNewsId}`, {
        method: "PUT",
        body: JSON.stringify(article)
      });
      Object.assign(existing, article);
      showToast("Yangilik yangilandi.");
    } else {
      const result = await adminApi("/api/admin/news", {
        method: "POST",
        body: JSON.stringify(article)
      });
      adminState.content.news.unshift(result.article);
      showToast("Yangi xabar nashr qilindi.");
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
  document.getElementById("newsDateInput").value = new Date().toISOString().slice(0, 10);
  document.getElementById("newsAuthorInput").value = "Agentlik Matbuot Xizmati";
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

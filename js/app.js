"use strict";

const translations = {
  uz: {
    agency_name: "AGROSANOATNI\nRIVOJLANTIRISH\nAGENTLIGI",
    nav_home: "Bosh sahifa",
    nav_about: "Agentlik haqida",
    nav_news: "Matbuot markazi",
    nav_contact: "Bog‘lanish",
    leader_director: "Agentlik rahbari",
    leader_first_deputy: "Birinchi o‘rinbosar",
    leader_deputy: "Direktor o‘rinbosari",
    leader_advisor: "Direktor maslahatchisi",
    powers: "Vakolatlari:",
    reception: "Qabul vaqti:",
    director_photo: "Direktor rasmi",
    no_data: "Ma’lumot kiritilmagan",
    schedule_missing: "Belgilanmagan",
    email_missing: "Email kiritilmagan",
    read_more: "Batafsil o‘qish",
    news_item: "Xabar",
    press_service: "Agentlik Matbuot Xizmati"
  },
  ru: {
    agency_name: "АГЕНТСТВО\nРАЗВИТИЯ\nАГРОПРОМЫШЛЕННОСТИ",
    nav_home: "Главная",
    nav_about: "Об агентстве",
    nav_news: "Пресс-центр",
    nav_contact: "Контакты",
    leader_director: "Руководитель агентства",
    leader_first_deputy: "Первый заместитель",
    leader_deputy: "Заместитель директора",
    leader_advisor: "Советник директора",
    powers: "Полномочия:",
    reception: "Приёмные часы:",
    director_photo: "Фото директора",
    no_data: "Информация не указана",
    schedule_missing: "Не указано",
    email_missing: "Email не указан",
    read_more: "Подробнее",
    news_item: "Новость",
    press_service: "Пресс-служба агентства"
  },
  en: {
    agency_name: "AGRIBUSINESS\nDEVELOPMENT\nAGENCY",
    nav_home: "Home",
    nav_about: "About agency",
    nav_news: "Press center",
    nav_contact: "Contact",
    leader_director: "Head of agency",
    leader_first_deputy: "First deputy",
    leader_deputy: "Deputy director",
    leader_advisor: "Director’s adviser",
    powers: "Responsibilities:",
    reception: "Reception hours:",
    director_photo: "Director photo",
    no_data: "Information not provided",
    schedule_missing: "Not specified",
    email_missing: "Email not provided",
    read_more: "Read more",
    news_item: "News",
    press_service: "Agency Press Service"
  }
};

let loadedContent = null;

document.addEventListener("DOMContentLoaded", async () => {
  initThemeToggle();
  initLanguageSwitcher();
  initMobileMenu();
  initSearch();
  initContactForm();
  initShareLinks();

  const needsContent = document.querySelector(
    ".region-sidebar, .leadership-grid, #newsListContainer, #articleBody, #homeNewsList"
  );
  if (!needsContent) return;

  try {
    const content = await loadContent();
    loadedContent = content;
    renderDynamicContent();
  } catch (error) {
    console.error("Kontentni yuklashda xato:", error);
    showDataError("Ma’lumotlarni yuklab bo‘lmadi. Sahifani yangilab ko‘ring.");
  }
});

async function loadContent() {
  const response = await fetch("/api/content", {
    headers: { Accept: "application/json" },
    cache: "no-store"
  });
  if (!response.ok) throw new Error(`API ${response.status}`);
  const data = await response.json();
  if (!data || typeof data !== "object") throw new Error("Kontent formati noto‘g‘ri");
  return data;
}

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function currentLanguage() {
  const language = localStorage.getItem("agro_language") || "uz";
  return translations[language] ? language : "uz";
}

function localizedValue(record, field, language = currentLanguage()) {
  if (language === "uz") return record?.[field] || "";
  return record?.translations?.[language]?.[field] || record?.[field] || "";
}

function translated(key, language = currentLanguage()) {
  return translations[language]?.[key] || translations.uz[key] || key;
}

function renderDynamicContent() {
  if (!loadedContent) return;
  renderRegionalMap(loadedContent.regions || {});
  renderLeadership(loadedContent.leadership || []);
  renderNews(loadedContent.news || []);
}

function icon(className) {
  const node = document.createElement("i");
  node.className = className;
  node.setAttribute("aria-hidden", "true");
  return node;
}

function showDataError(message) {
  document.querySelectorAll(".region-sidebar, .leadership-grid, #newsListContainer, #articleBody, #homeNewsList")
    .forEach(container => {
      container.replaceChildren(element("p", "status-message status-error", message));
    });
}

function initLanguageSwitcher() {
  const saved = localStorage.getItem("agro_language") || "uz";
  applyLanguage(saved);
  document.querySelectorAll(".lang-btn").forEach(button => {
    button.classList.toggle("active", button.dataset.lang === saved);
    button.addEventListener("click", () => {
      const language = translations[button.dataset.lang] ? button.dataset.lang : "uz";
      localStorage.setItem("agro_language", language);
      document.querySelectorAll(".lang-btn").forEach(item => {
        item.classList.toggle("active", item === button);
      });
      applyLanguage(language);
      renderDynamicContent();
    });
  });
}

function applyLanguage(language) {
  const dictionary = translations[language] || translations.uz;
  document.documentElement.lang = language;
  document.querySelectorAll("[data-i18n]").forEach(node => {
    const value = dictionary[node.dataset.i18n];
    if (!value) return;
    if (node.dataset.i18n === "agency_name") {
      node.replaceChildren();
      value.split("\n").forEach((line, index) => {
        if (index) node.append(document.createElement("br"));
        node.append(document.createTextNode(line));
      });
    } else {
      node.textContent = value;
    }
  });
}

function initThemeToggle() {
  const button = document.getElementById("themeToggleBtn");
  const theme = localStorage.getItem("agro_theme") || "light";
  document.documentElement.dataset.theme = theme;
  updateThemeButton(button, theme);
  if (!button) return;
  button.addEventListener("click", () => {
    const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    localStorage.setItem("agro_theme", next);
    updateThemeButton(button, next);
  });
}

function updateThemeButton(button, theme) {
  if (!button) return;
  button.replaceChildren(icon(theme === "dark" ? "fas fa-sun" : "fas fa-moon"));
  button.setAttribute("aria-label", theme === "dark" ? "Kunduzgi rejimni yoqish" : "Tungi rejimni yoqish");
  button.title = button.getAttribute("aria-label");
}

function initMobileMenu() {
  const button = document.getElementById("mobileMenuBtn");
  const menu = document.getElementById("navMenu");
  if (!button || !menu) return;

  const close = () => {
    menu.classList.remove("active");
    button.setAttribute("aria-expanded", "false");
    button.replaceChildren(icon("fas fa-bars"));
  };

  button.addEventListener("click", () => {
    const opening = !menu.classList.contains("active");
    menu.classList.toggle("active", opening);
    button.setAttribute("aria-expanded", String(opening));
    button.replaceChildren(icon(opening ? "fas fa-times" : "fas fa-bars"));
  });
  menu.querySelectorAll("a").forEach(link => link.addEventListener("click", close));
  document.addEventListener("keydown", event => {
    if (event.key === "Escape") close();
  });
}

function renderRegionalMap(regions) {
  const sidebar = document.querySelector(".region-sidebar");
  if (!sidebar) return;
  sidebar.replaceChildren();
  const entries = Object.entries(regions);
  if (!entries.length) {
    sidebar.append(element("p", "status-message", "Hududiy ma’lumotlar topilmadi."));
    return;
  }

  const fields = {
    name: document.getElementById("officeName"),
    head: document.getElementById("officeHead"),
    phone: document.getElementById("officePhone"),
    address: document.getElementById("officeAddress"),
    projects: document.getElementById("officeProjects")
  };

  const selectRegion = (button, data) => {
    sidebar.querySelectorAll(".region-btn").forEach(item => {
      const selected = item === button;
      item.classList.toggle("active", selected);
      item.setAttribute("aria-pressed", String(selected));
    });
    Object.entries(fields).forEach(([key, node]) => {
      if (node) node.textContent = localizedValue(data, key) || translated("no_data");
    });
  };

  entries.forEach(([key, data], index) => {
    const button = element("button", "region-btn");
    button.type = "button";
    button.dataset.region = key;
    button.append(element("span", "", localizedValue(data, "name")), icon("fas fa-chevron-right"));
    button.addEventListener("click", () => selectRegion(button, data));
    sidebar.append(button);
    if (index === 0) selectRegion(button, data);
  });
}

function renderLeadership(leadership) {
  const grid = document.querySelector(".leadership-grid");
  if (!grid) return;
  grid.replaceChildren();
  if (!leadership.length) {
    grid.append(element("p", "status-message", "Rahbariyat ma’lumotlari topilmadi."));
    return;
  }

  leadership.forEach((person, index) => {
    const role = String(person.role || "").toLocaleLowerCase("uz");
    const tier = role.includes("birinchi o‘rinbosar") || role.includes("birinchi o'rinbosar")
      ? "first-deputy"
      : role.includes("o‘rinbosar") || role.includes("o'rinbosar")
        ? "deputy"
        : role.includes("maslahatch")
          ? "advisor"
          : "director";
    const tierLabel = {
      director: translated("leader_director"),
      "first-deputy": translated("leader_first_deputy"),
      deputy: translated("leader_deputy"),
      advisor: translated("leader_advisor")
    }[tier];
    const name = localizedValue(person, "name");
    const displayRole = localizedValue(person, "role");

    const card = element("article", `leader-card leader-card-${tier}`);
    card.dataset.tier = tier;
    const cardTop = element("div", "leader-card-top");
    cardTop.append(
      element("span", "leader-tier", tierLabel),
      element("span", "leader-index", String(index + 1).padStart(2, "0"))
    );
    const media = element("div", "leader-avatar leader-media");
    if (person.photo) {
      const photo = document.createElement("img");
      photo.className = "leader-photo";
      photo.src = person.photo;
      photo.alt = `${name} — ${displayRole}`;
      photo.loading = tier === "director" ? "eager" : "lazy";
      photo.decoding = "async";
      media.append(photo);
    } else {
      media.classList.add("leader-photo-placeholder");
      media.append(icon("fas fa-camera"));
      if (tier === "director") media.append(element("span", "leader-photo-hint", translated("director_photo")));
    }
    const identity = element("div", "leader-identity");
    identity.append(element("h3", "leader-name", name), element("div", "leader-role", displayRole));
    card.append(cardTop, element("div", "leader-profile", ""));
    card.querySelector(".leader-profile").append(media, identity);

    const description = element("p", "leader-description");
    description.append(element("strong", "", `${translated("powers")} `), document.createTextNode(localizedValue(person, "desc") || translated("no_data")));
    card.append(description);

    const contacts = element("div", "leader-contact");
    const hours = element("p");
    hours.append(icon("fas fa-clock"), element("strong", "", ` ${translated("reception")} `), document.createTextNode(localizedValue(person, "hours") || translated("schedule_missing")));
    const email = element("p");
    email.append(icon("fas fa-envelope"), document.createTextNode(` ${person.email || translated("email_missing")}`));
    contacts.append(hours, email);
    card.append(contacts);
    grid.append(card);
  });
}

function renderNews(allNews) {
  const language = currentLanguage();
  const query = new URLSearchParams(location.search).get("q")?.trim().toLocaleLowerCase(language) || "";
  const filteredNews = query
    ? allNews.filter(article => ["title", "excerpt", "category", "content"]
      .some(field => localizedValue(article, field, language).toLocaleLowerCase(language).includes(query)))
    : allNews;

  const list = document.getElementById("newsListContainer");
  if (list) {
    list.replaceChildren();
    const result = document.getElementById("searchResultSummary");
    if (result) {
      result.textContent = query
        ? `“${query}” bo‘yicha ${filteredNews.length} ta natija topildi.`
        : `${filteredNews.length} ta rasmiy xabar.`;
    }
    filteredNews.forEach(article => list.append(buildNewsCard(article)));
    if (!filteredNews.length) list.append(element("p", "status-message", "Qidiruv bo‘yicha yangilik topilmadi."));
  }

  const homeList = document.getElementById("homeNewsList");
  if (homeList) {
    homeList.replaceChildren();
    allNews.slice(0, 2).forEach(article => homeList.append(buildNewsCard(article)));
  }

  renderArticleDetail(allNews);
}

function buildNewsCard(article) {
  const card = element("article", "news-card");
  const image = element("img", "news-img");
  image.src = article.image || "assets/hero_agri.jpg";
  const titleText = localizedValue(article, "title");
  image.alt = titleText;
  image.loading = "lazy";

  const content = element("div", "news-content");
  const header = element("div");
  const meta = element("div", "news-date");
  meta.append(icon("far fa-calendar-alt"), document.createTextNode(` ${formatDate(article.date)} · ${localizedValue(article, "category") || translated("news_item")}`));
  const title = element("h3", "news-title");
  const link = element("a", "", titleText);
  link.href = `news-detail.html?id=${encodeURIComponent(article.id)}`;
  title.append(link);
  header.append(meta, title);
  content.append(header, element("p", "news-excerpt", localizedValue(article, "excerpt")));
  const more = element("a", "btn btn-secondary news-more", `${translated("read_more")} `);
  more.href = link.href;
  more.append(icon("fas fa-arrow-right"));
  content.append(more);
  card.append(image, content);
  return card;
}

function renderArticleDetail(allNews) {
  const body = document.getElementById("articleBody");
  if (!body) return;
  const requestedId = Number(new URLSearchParams(location.search).get("id"));
  const article = allNews.find(item => Number(item.id) === requestedId) || allNews[0];
  if (!article) {
    body.replaceChildren(element("p", "status-message", "Yangilik topilmadi."));
    return;
  }

  const title = document.getElementById("articleTitle");
  const date = document.getElementById("articleDate");
  const category = document.getElementById("articleCategory");
  const author = document.getElementById("articleAuthor");
  const hero = document.getElementById("articleHeroImg");
  const titleText = localizedValue(article, "title");
  if (title) title.textContent = titleText;
  if (date) date.textContent = formatDate(article.date);
  if (category) category.textContent = localizedValue(article, "category") || translated("news_item");
  if (author) author.textContent = localizedValue(article, "author") || translated("press_service");
  if (hero) {
    hero.src = article.image || "assets/hero_agri.jpg";
    hero.alt = titleText;
  }
  document.title = `${titleText} | Agrosanoat agentligi`;
  body.replaceChildren();
  String(localizedValue(article, "content") || localizedValue(article, "excerpt"))
    .split(/\n\s*\n/u)
    .filter(Boolean)
    .forEach(paragraph => body.append(element("p", "", paragraph)));
}

function formatDate(value) {
  if (!/^\d{4}-\d{2}-\d{2}$/u.test(String(value))) return value || "";
  const date = new Date(`${value}T00:00:00Z`);
  const locales = { uz: "uz-UZ", ru: "ru-RU", en: "en-GB" };
  return new Intl.DateTimeFormat(locales[currentLanguage()], { day: "numeric", month: "long", year: "numeric", timeZone: "UTC" }).format(date);
}

function initSearch() {
  const input = document.getElementById("quickSearchInput");
  const button = document.getElementById("quickSearchButton");
  if (!input) return;
  const submit = () => {
    const query = input.value.trim();
    if (query) location.href = `news.html?q=${encodeURIComponent(query)}`;
  };
  input.addEventListener("keydown", event => {
    if (event.key === "Enter") submit();
  });
  button?.addEventListener("click", submit);
}

function initContactForm() {
  const form = document.getElementById("contactForm");
  const status = document.getElementById("contactFormStatus");
  if (!form || !status) return;
  form.addEventListener("submit", async event => {
    event.preventDefault();
    const submit = form.querySelector("button[type='submit']");
    submit.disabled = true;
    status.className = "status-message";
    status.textContent = "Murojaat yuborilmoqda…";
    const formData = new FormData(form);
    try {
      const response = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(Object.fromEntries(formData.entries()))
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || "Murojaat yuborilmadi");
      form.reset();
      status.className = "status-message status-success";
      status.textContent = `Murojaatingiz qabul qilindi. Raqam: ${result.reference}`;
    } catch (error) {
      status.className = "status-message status-error";
      status.textContent = error.message;
    } finally {
      submit.disabled = false;
    }
  });
}

function initShareLinks() {
  const telegram = document.getElementById("shareTelegram");
  const facebook = document.getElementById("shareFacebook");
  if (!telegram && !facebook) return;
  const url = encodeURIComponent(location.href);
  const title = encodeURIComponent(document.title);
  if (telegram) telegram.href = `https://t.me/share/url?url=${url}&text=${title}`;
  if (facebook) facebook.href = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
}

"use strict";

const translations = {
  uz: {
    agency_name: "AGROSANOATNI\nRIVOJLANTIRISH\nAGENTLIGI",
    nav_home: "Bosh sahifa",
    nav_about: "Agentlik haqida",
    nav_news: "Matbuot markazi",
    nav_contact: "Bog‘lanish"
  },
  ru: {
    agency_name: "АГЕНТСТВО\nРАЗВИТИЯ\nАГРОПРОМЫШЛЕННОСТИ",
    nav_home: "Главная",
    nav_about: "Об агентстве",
    nav_news: "Пресс-центр",
    nav_contact: "Контакты"
  },
  en: {
    agency_name: "AGRIBUSINESS\nDEVELOPMENT\nAGENCY",
    nav_home: "Home",
    nav_about: "About agency",
    nav_news: "Press center",
    nav_contact: "Contact"
  }
};

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
    renderRegionalMap(content.regions || {});
    renderLeadership(content.leadership || []);
    renderNews(content.news || []);
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
  const theme = localStorage.getItem("agro_theme") || "dark";
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
      if (node) node.textContent = data[key] || "Ma’lumot kiritilmagan";
    });
  };

  entries.forEach(([key, data], index) => {
    const button = element("button", "region-btn");
    button.type = "button";
    button.dataset.region = key;
    button.append(element("span", "", data.name.replace(/ Boshqarmasi$/u, "")), icon("fas fa-chevron-right"));
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
      director: "Agentlik rahbari",
      "first-deputy": "Birinchi o‘rinbosar",
      deputy: "Direktor o‘rinbosari",
      advisor: "Direktor maslahatchisi"
    }[tier];

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
      photo.alt = `${person.name} — ${person.role}`;
      photo.loading = tier === "director" ? "eager" : "lazy";
      photo.decoding = "async";
      media.append(photo);
    } else {
      media.classList.add("leader-photo-placeholder");
      media.append(icon("fas fa-camera"));
      if (tier === "director") media.append(element("span", "leader-photo-hint", "Direktor rasmi"));
    }
    const identity = element("div", "leader-identity");
    identity.append(element("h3", "leader-name", person.name), element("div", "leader-role", person.role));
    card.append(cardTop, element("div", "leader-profile", ""));
    card.querySelector(".leader-profile").append(media, identity);

    const description = element("p", "leader-description");
    description.append(element("strong", "", "Vakolatlari: "), document.createTextNode(person.desc || "Ma’lumot kiritilmagan"));
    card.append(description);

    const contacts = element("div", "leader-contact");
    const hours = element("p");
    hours.append(icon("fas fa-clock"), element("strong", "", " Qabul vaqti: "), document.createTextNode(person.hours || "Belgilanmagan"));
    const email = element("p");
    email.append(icon("fas fa-envelope"), document.createTextNode(` ${person.email || "Email kiritilmagan"}`));
    contacts.append(hours, email);
    card.append(contacts);
    grid.append(card);
  });
}

function renderNews(allNews) {
  const query = new URLSearchParams(location.search).get("q")?.trim().toLocaleLowerCase("uz") || "";
  const filteredNews = query
    ? allNews.filter(article => [article.title, article.excerpt, article.category, article.content]
      .some(value => String(value || "").toLocaleLowerCase("uz").includes(query)))
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
  image.alt = article.title;
  image.loading = "lazy";

  const content = element("div", "news-content");
  const header = element("div");
  const meta = element("div", "news-date");
  meta.append(icon("far fa-calendar-alt"), document.createTextNode(` ${formatDate(article.date)} · ${article.category || "Xabar"}`));
  const title = element("h3", "news-title");
  const link = element("a", "", article.title);
  link.href = `news-detail.html?id=${encodeURIComponent(article.id)}`;
  title.append(link);
  header.append(meta, title);
  content.append(header, element("p", "news-excerpt", article.excerpt || ""));
  const more = element("a", "btn btn-secondary news-more", "Batafsil o‘qish ");
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
  if (title) title.textContent = article.title;
  if (date) date.textContent = formatDate(article.date);
  if (category) category.textContent = article.category || "Xabar";
  if (author) author.textContent = article.author || "Agentlik Matbuot Xizmati";
  if (hero) {
    hero.src = article.image || "assets/hero_agri.jpg";
    hero.alt = article.title;
  }
  document.title = `${article.title} | Agrosanoat agentligi`;
  body.replaceChildren();
  String(article.content || article.excerpt || "")
    .split(/\n\s*\n/u)
    .filter(Boolean)
    .forEach(paragraph => body.append(element("p", "", paragraph)));
}

function formatDate(value) {
  if (!/^\d{4}-\d{2}-\d{2}$/u.test(String(value))) return value || "";
  const date = new Date(`${value}T00:00:00Z`);
  return new Intl.DateTimeFormat("uz-UZ", { day: "numeric", month: "long", year: "numeric", timeZone: "UTC" }).format(date);
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

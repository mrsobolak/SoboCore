const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

const toast = $("#toast");

function showToast(text) {
  toast.textContent = text;
  toast.hidden = false;
  clearTimeout(showToast._t);
  showToast._t = setTimeout(() => (toast.hidden = true), 1600);
}

function setTheme(theme) {
  if (theme === "light") {
    document.documentElement.setAttribute("data-theme", "light");
    $("#themeIcon").textContent = "☀";
  } else {
    document.documentElement.removeAttribute("data-theme");
    $("#themeIcon").textContent = "☾";
  }
  localStorage.setItem("theme", theme);
}

(function initTheme() {
  const saved = localStorage.getItem("theme");
  if (saved) return setTheme(saved);
  const prefersLight = window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches;
  setTheme(prefersLight ? "light" : "dark");
})();

$("#themeBtn").addEventListener("click", () => {
  const isLight = document.documentElement.getAttribute("data-theme") === "light";
  setTheme(isLight ? "dark" : "light");
});

$("#year").textContent = new Date().getFullYear();

const menuBtn = $("#menuBtn");
const mobileNav = $("#mobileNav");

function closeMobileNav() {
  menuBtn.setAttribute("aria-expanded", "false");
  mobileNav.hidden = true;
}

menuBtn.addEventListener("click", () => {
  const expanded = menuBtn.getAttribute("aria-expanded") === "true";
  menuBtn.setAttribute("aria-expanded", String(!expanded));
  mobileNav.hidden = expanded;
});

$$(".mobile-nav a").forEach(a => a.addEventListener("click", closeMobileNav));

$$("button.copy").forEach(btn => {
  btn.addEventListener("click", async () => {
    const text = btn.getAttribute("data-copy") || "";
    try {
      await navigator.clipboard.writeText(text);
      showToast("Copied ✅");
    } catch {
      showToast("Copy failed");
    }
  });
});

const io = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add("is-visible");
      io.unobserve(e.target);
    }
  });
}, { threshold: 0.12 });

$$(".reveal").forEach(el => io.observe(el));

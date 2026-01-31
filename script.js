const themeBtn = document.getElementById("themeBtn");
const menuBtn = document.getElementById("menuBtn");
const mobileMenu = document.getElementById("mobileMenu");

function applyTheme(mode) {
  document.body.classList.toggle("light", mode === "light");
  localStorage.setItem("sobo_theme", mode);
  if (themeBtn) themeBtn.setAttribute("aria-pressed", mode === "light" ? "true" : "false");
}

function initTheme() {
  const saved = localStorage.getItem("sobo_theme");
  if (saved === "light" || saved === "dark") {
    applyTheme(saved);
  } else {
    applyTheme("dark");
  }
}

function closeMobileMenu() {
  if (!mobileMenu) return;
  mobileMenu.classList.remove("open");
  mobileMenu.setAttribute("aria-hidden", "true");
}

function toggleMobileMenu() {
  if (!mobileMenu) return;
  const open = mobileMenu.classList.toggle("open");
  mobileMenu.setAttribute("aria-hidden", open ? "false" : "true");
}

themeBtn?.addEventListener("click", () => {
  const isLight = document.body.classList.contains("light");
  applyTheme(isLight ? "dark" : "light");
});

menuBtn?.addEventListener("click", toggleMobileMenu);

document.querySelectorAll(".mLink").forEach((link) => {
  link.addEventListener("click", closeMobileMenu);
});

window.addEventListener("resize", () => {
  if (window.innerWidth > 760) closeMobileMenu();
});

document.addEventListener("click", (e) => {
  if (!mobileMenu || mobileMenu.getAttribute("aria-hidden") === "true") return;
  const t = e.target;
  const clickedMenu = mobileMenu.contains(t);
  const clickedBtn = menuBtn && menuBtn.contains(t);
  if (!clickedMenu && !clickedBtn) closeMobileMenu();
});

initTheme();
closeMobileMenu();

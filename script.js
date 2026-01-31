const themeBtn = document.getElementById("themeBtn");
const menuBtn = document.getElementById("menuBtn");
const mobileMenu = document.getElementById("mobileMenu");

function setTheme(mode) {
  const isLight = mode === "light";
  document.body.classList.toggle("light", isLight);
  localStorage.setItem("sobo_theme", mode);
}

  function initTheme() {
  const saved = localStorage.getItem("sobo_theme");
  if (saved === "light" || saved === "dark") {
    setTheme(saved);
    return;
  }
  // default dark
  setTheme("dark");
}

themeBtn?.addEventListener("click", () => {
  const nowLight = document.body.classList.contains("light");
  setTheme(nowLight ? "dark" : "light");
});

menuBtn?.addEventListener("click", () => {
  const open = mobileMenu.getAttribute("aria-hidden") === "false";
  mobileMenu.setAttribute("aria-hidden", open ? "true" : "false");
  mobileMenu.style.display = open ? "none" : "block";
});

document.querySelectorAll(".mLink").forEach((link) => {
  link.addEventListener("click", () => {
    mobileMenu.setAttribute("aria-hidden", "true");
    mobileMenu.style.display = "none";
  });
});

initTheme();

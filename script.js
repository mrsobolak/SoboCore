const menuBtn = document.getElementById("menuBtn");
const mobileMenu = document.getElementById("mobileMenu");

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

closeMobileMenu();

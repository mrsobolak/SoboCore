const menuBtn = document.getElementById("menuBtn");
const mobileMenu = document.getElementById("mobileMenu");
<<<<<<< codex/remove-project-placeholder-text-rh11cr
=======
const countdownTarget = new Date(2026, 1, 2, 0, 0, 0);
const countdownFields = {
  days: document.getElementById("countDays"),
  hours: document.getElementById("countHours"),
  minutes: document.getElementById("countMinutes"),
  seconds: document.getElementById("countSeconds"),
};
const countdownNote = document.getElementById("countdownNote");

>>>>>>> main
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

function updateCountdown() {
  const { days, hours, minutes, seconds } = countdownFields;
  if (!days || !hours || !minutes || !seconds) return;
  const now = new Date();
  const diff = countdownTarget.getTime() - now.getTime();
  if (diff <= 0) {
    days.textContent = "0";
    hours.textContent = "0";
    minutes.textContent = "0";
    seconds.textContent = "0";
    if (countdownNote) {
      countdownNote.textContent = "SoboAI is live.";
    }
    return;
  }

  const totalSeconds = Math.floor(diff / 1000);
  const remainingDays = Math.floor(totalSeconds / 86400);
  const remainingHours = Math.floor((totalSeconds % 86400) / 3600);
  const remainingMinutes = Math.floor((totalSeconds % 3600) / 60);
  const remainingSeconds = totalSeconds % 60;

  days.textContent = remainingDays.toString();
  hours.textContent = remainingHours.toString().padStart(2, "0");
  minutes.textContent = remainingMinutes.toString().padStart(2, "0");
  seconds.textContent = remainingSeconds.toString().padStart(2, "0");
}

updateCountdown();
setInterval(updateCountdown, 1000);

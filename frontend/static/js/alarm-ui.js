// Live clock and date display on the Overview dashboard
function updateClock() {
  const now = new Date();
  document.querySelectorAll("[data-live-clock]").forEach((el) => {
    el.textContent = now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
  });
  document.querySelectorAll("[data-live-date]").forEach((el) => {
    el.textContent = now.toLocaleDateString(undefined, { weekday: "long", year: "numeric", month: "long", day: "numeric" });
  });
}

if (document.querySelector("[data-live-clock], [data-live-date]")) {
  updateClock();
  setInterval(updateClock, 1000);
}

const brand = document.querySelector(".site-header .brand");
let frame;
let lastProgress;

function renderBrand() {
  frame = undefined;
  const progress = Math.min(1, Math.max(0, (window.scrollY - 8) / 72));
  if (progress === lastProgress) return;
  lastProgress = progress;
  brand.style.setProperty("--brand-progress", progress);
  brand.toggleAttribute("data-compact", progress >= 0.5);
}

function scheduleBrand() {
  frame ??= window.requestAnimationFrame(renderBrand);
}

renderBrand();
window.addEventListener("scroll", scheduleBrand, { passive: true });
window.addEventListener("pageshow", scheduleBrand);

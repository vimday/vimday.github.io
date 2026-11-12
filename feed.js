const filters = document.querySelector("#filters");
const notes = [...document.querySelectorAll("#notes [data-category]")];
const empty = document.querySelector("#empty");
const replays = [...document.querySelectorAll("[data-replay]")];

if (filters && empty && notes.length > 0) {
  const buttons = [...filters.querySelectorAll("button")];
  function showCategory(category) {
    for (const filter of buttons) {
      filter.setAttribute("aria-pressed", String(filter.dataset.filter === category));
    }
    for (const note of notes) {
      note.hidden = category !== "all" && note.dataset.category !== category;
    }
    empty.hidden = notes.some((note) => !note.hidden);
  }

  filters.hidden = false;
  filters.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-filter]");
    if (button) showCategory(button.dataset.filter);
  });
}

function setupReplay(panel) {
  const frames = [...panel.querySelectorAll("[data-frame]")];
  const controls = panel.querySelector("[data-replay-controls]");
  const slider = controls.querySelector("input");
  const ticks = [...controls.querySelectorAll(".replay-ticks span")];
  const play = controls.querySelector("button");
  const label = play.lastElementChild;
  let timer;

  function showFrame(index) {
    frames.forEach((frame, position) => {
      frame.toggleAttribute("data-active", position === index);
      ticks[position].classList.toggle("is-current", position === index);
    });
    slider.value = index;
    slider.setAttribute("aria-valuetext", `${ticks[index].textContent} · ${frames[index].querySelector("h3").textContent}`);
  }

  function stop() {
    window.clearInterval(timer);
    timer = undefined;
    play.classList.remove("is-playing");
    label.textContent = play.dataset.play;
  }

  slider.addEventListener("input", () => {
    stop();
    showFrame(slider.valueAsNumber);
  });
  play.addEventListener("click", () => {
    if (timer !== undefined) {
      stop();
      return;
    }
    if (slider.value === slider.max) showFrame(0);
    play.classList.add("is-playing");
    label.textContent = play.dataset.pause;
    timer = window.setInterval(() => {
      const next = slider.valueAsNumber + 1;
      showFrame(next);
      if (next === Number(slider.max)) stop();
    }, 1650);
  });

  panel.addEventListener("toggle", () => {
    if (!panel.open) stop();
  });

  showFrame(0);
  panel.classList.add("is-enhanced");
  controls.hidden = false;
  return stop;
}

if (replays.length) {
  const stopReplays = replays.map(setupReplay);
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) stopReplays.forEach((stop) => stop());
  });
}

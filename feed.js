const homeNotes = document.currentScript.dataset.homeNotes;
if (homeNotes !== undefined) {
  const noteAnchors = new Set(homeNotes ? ["feed", "notes", ...homeNotes.split(" ")] : []);
  function followMovedSection() {
    const section = window.location.hash.slice(1);
    const path = section === "research-walkthrough" ? "products/" : noteAnchors.has(section) ? "research/" : "";
    if (path) window.location.replace(path + window.location.hash);
  }
  followMovedSection();
  window.addEventListener("hashchange", followMovedSection);
}

const filters = document.querySelector("#filters");
const notes = [...document.querySelectorAll("#notes [data-category]")];
const empty = document.querySelector("#empty");

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

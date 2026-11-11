const filters = document.querySelector("#filters");
const notes = [...document.querySelectorAll("#notes [data-category]")];
const empty = document.querySelector("#empty");

if (filters && empty && notes.length > 0) {
  const buttons = [...filters.querySelectorAll("button")];
  filters.hidden = false;
  filters.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-filter]");
    if (!button) return;

    const category = button.dataset.filter;
    for (const filter of buttons) {
      filter.setAttribute("aria-pressed", String(filter === button));
    }
    for (const note of notes) {
      note.hidden = category !== "all" && note.dataset.category !== category;
    }
    empty.hidden = notes.some((note) => !note.hidden);
  });
}

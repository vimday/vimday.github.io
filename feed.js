const filters = document.querySelector("#filters");
const notes = [...document.querySelectorAll("#notes [data-category]")];
const empty = document.querySelector("#empty");
const workbench = document.querySelector("[data-workbench]");

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
  document.querySelector("[data-show-note]")?.addEventListener("click", () => showCategory("all"));
}

if (workbench) {
  const tablist = workbench.querySelector('[role="tablist"]');
  const tabs = [...tablist.querySelectorAll('[role="tab"]')];
  const panels = tabs.map((tab) => document.getElementById(tab.getAttribute("aria-controls")));

  function selectTab(index) {
    tabs.forEach((tab, position) => {
      const active = index === position;
      tab.setAttribute("aria-selected", String(active));
      tab.tabIndex = active ? 0 : -1;
      panels[position].hidden = !active;
    });
  }

  tabs.forEach((tab, index) => {
    const panel = panels[index];
    panel.setAttribute("role", "tabpanel");
    panel.setAttribute("aria-labelledby", tab.id);
    panel.tabIndex = 0;
    tab.addEventListener("click", () => selectTab(index));
    tab.addEventListener("keydown", (event) => {
      let next;
      switch (event.key) {
        case "ArrowLeft": next = (index - 1 + tabs.length) % tabs.length; break;
        case "ArrowRight": next = (index + 1) % tabs.length; break;
        case "Home": next = 0; break;
        case "End": next = tabs.length - 1; break;
        default: return;
      }
      event.preventDefault();
      selectTab(next);
      tabs[next].focus();
    });
  });

  selectTab(0);
  workbench.classList.add("is-enhanced");
  tablist.hidden = false;
}

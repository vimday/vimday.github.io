(() => {
  const feed = document.querySelector("#notes");
  if (!feed) return;

  const zh = document.documentElement.lang.startsWith("zh");
  const locale = zh ? "zh" : "en";
  const categories = zh
    ? { markets: "市场", data: "数据", tools: "工具" }
    : { markets: "Markets", data: "Data", tools: "Tools" };
  const node = (tag, text, className) => {
    const el = document.createElement(tag);
    if (text) el.textContent = text;
    if (className) el.className = className;
    return el;
  };

  function parse(entry) {
    if (!entry || typeof entry !== "object") return null;
    const { date, category, source } = entry;
    const copy = entry[locale];
    if (typeof date !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(date)
        || !Object.hasOwn(categories, category) || !copy) return null;
    if (["title", "summary", "risk"].some(key => typeof copy[key] !== "string" || !copy[key].trim())) return null;
    if (typeof source !== "string") return null;
    try {
      const url = new URL(source);
      if (url.protocol !== "https:" || url.username || url.password) return null;
      return { date, category, copy, url };
    } catch {
      return null;
    }
  }

  function card({ date, category, copy, url }) {
    const item = node("article", "", "project");
    const heading = node("h3", copy.title);
    const day = node("time", date);
    day.dateTime = date;
    const label = node("p", categories[category] + " / ", "tag");
    label.append(day);
    const risk = node("p", (zh ? "失效条件：" : "What could invalidate it: ") + copy.risk);
    const link = node("a", zh ? "看原始来源 ↗" : "View original source ↗");
    link.href = url.href;
    item.append(label, heading, node("p", copy.summary), risk, link);
    return item;
  }

  fetch(feed.dataset.feed)
    .then(response => {
      if (!response.ok) throw new Error("Feed unavailable");
      return response.json();
    })
    .then(raw => {
      if (!Array.isArray(raw)) throw new Error("Invalid feed");
      const notes = raw.map(parse).filter(Boolean).sort((a, b) => b.date.localeCompare(a.date));
      if (!notes.length && raw.length) throw new Error("Invalid notes");
      if (notes.length) feed.replaceChildren(...notes.map(card));
    })
    .catch(() => {
      feed.replaceChildren(node("p", zh ? "暂时无法加载笔记，请稍后再试。" : "Notes are temporarily unavailable. Try again later.", "empty"));
    });
})();

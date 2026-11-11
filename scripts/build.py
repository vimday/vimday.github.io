"""Build the English and Simplified Chinese pages."""

import json
import re
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CONTACT = "hi@alphawink.com"
GITHUB = "https://github.com/vimday"
ALEPH = "https://github.com/AlephTX/aleph-tx"
ROUTES = ("", "products/", "about/")

COPY = {
    "en": {
        "nav": ("Alpha", "Products", "About"),
        "skip": "Skip to content",
        "nav_label": "Site navigation",
        "alpha": {
            "title": ("Find the", "signal."),
            "intro": "Research notes on markets, robotics data, and the tools used to investigate them.",
            "browse": "Explore the notes",
            "method": "Before calling it an opportunity",
            "questions": (
                ("Observe", "What changed?"),
                ("Verify", "What can you reproduce?"),
                ("Revisit", "What would change your mind?"),
            ),
            "feed": "Research notes",
            "filters": {"all": "All", "markets": "Markets", "data": "Robotics data", "tools": "Tools"},
            "empty": "No notes in this category yet.",
            "source": "Original source",
            "risk": "What to watch",
            "share": "Found something worth investigating?",
            "send": "Share a lead",
            "latest": "Latest note",
        },
        "products": {
            "title": "Tools for market research",
            "intro": "AlephTX replays market data to test execution assumptions. Oasis Agent traces decisions back to the evidence and risk checks behind them.",
            "aleph": (
                "Perpetual futures",
                "Study relative value across markets. Replay recorded data and check whether an idea holds up after fees, funding, and slippage.",
                ("Market data replay", "Execution and cost modeling", "Relative-value research"),
            ),
            "oasis": (
                "Research and risk",
                "Keep a record of what the agent observed, how it reached a decision, and which limits apply before execution.",
                ("Evidence records", "Decision replay", "Risk checks"),
            ),
            "source": "View source on GitHub",
            "status": "In development",
        },
        "about": {
            "title": "Robotics data and AI infrastructure",
            "intro": "I build data platforms for embodied AI, including the workflows that turn multimodal robot data into datasets that teams can validate and reuse.",
            "github": "GitHub profile",
            "work": "Engineering work",
            "work_areas": (
                ("Data platforms", "Pipelines for processing, annotating, validating, and versioning multimodal robot datasets."),
                ("AI infrastructure", "Distributed services that run data workflows and deliver datasets."),
                ("Workflow graph engine", "I built an engine from scratch to run robot data processing steps with explicit dependencies."),
                ("Advertising platform", "Go backend development for an advertising platform, from before I used coding agents in my daily work."),
            ),
            "tools": "Daily tools",
            "stack": (
                ("Coding agents", "Codex · Claude Code · MCP"),
                ("Terminal", "Herdr · Neovim · Linux · Git"),
                ("Systems", "Go · Rust · Python · Kubernetes · Docker"),
            ),
        },
    },
    "zh": {
        "nav": ("Alpha 机会", "产品", "关于"),
        "skip": "跳到正文",
        "nav_label": "网站导航",
        "alpha": {
            "title": ("寻找值得", "验证的机会。"),
            "intro": "记录市场、机器人数据和研究工具里的发现，附上核实线索和判断可能失效的条件。",
            "browse": "查看研究笔记",
            "method": "判断机会前，先问三件事",
            "questions": (
                ("观察", "发生了什么变化？"),
                ("核实", "哪些证据可以复现？"),
                ("复查", "什么会改变判断？"),
            ),
            "feed": "研究笔记",
            "filters": {"all": "全部", "markets": "市场", "data": "机器人数据", "tools": "工具"},
            "empty": "这个分类还没有笔记。",
            "source": "原始来源",
            "risk": "需要留意",
            "share": "有值得研究的线索？",
            "send": "分享线索",
            "latest": "最新笔记",
        },
        "products": {
            "title": "市场研究工具",
            "intro": "AlephTX 用市场数据回放检验执行假设。Oasis Agent 记录判断所依据的证据和风险检查。",
            "aleph": (
                "永续合约",
                "研究不同市场之间的相对价值。回放记录下来的行情，检查计入手续费、资金费率和滑点后，假设是否仍然成立。",
                ("市场数据回放", "执行和成本建模", "相对价值研究"),
            ),
            "oasis": (
                "研究与风控",
                "记录 Agent 看到了什么、如何得出判断，以及执行前要满足哪些风险约束。",
                ("证据记录", "决策回放", "风险检查"),
            ),
            "source": "在 GitHub 查看源码",
            "status": "开发中",
        },
        "about": {
            "title": "机器人数据与 AI 基础设施",
            "intro": "我做具身智能数据平台和 AI 基础设施，把多模态机器人数据处理成可校验、可复用的数据集。",
            "github": "GitHub 主页",
            "work": "工程经历",
            "work_areas": (
                ("数据平台", "构建多模态机器人数据流水线，覆盖处理、标注、质量校验和版本管理。"),
                ("AI 基础设施", "为数据流程的执行和数据集交付构建分布式服务。"),
                ("图流程引擎", "从零开发机器人数据处理引擎，用图表达处理步骤及依赖关系。"),
                ("广告平台", "早期手写代码时，参与过广告平台的 Go 后端开发。"),
            ),
            "tools": "日常工具",
            "stack": (
                ("编程 Agent", "Codex · Claude Code · MCP"),
                ("终端环境", "Herdr · Neovim · Linux · Git"),
                ("系统开发", "Go · Rust · Python · Kubernetes · Docker"),
            ),
        },
    },
}


def read_notes():
    notes = json.loads((ROOT / "opportunities.json").read_text(encoding="utf-8"))
    ids = set()
    for number, entry in enumerate(notes, 1):
        entry.setdefault("id", f"note-{number}")
        slug = entry["id"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or slug in ids:
            raise ValueError("Invalid or duplicate research note ID")
        ids.add(slug)
        date.fromisoformat(entry["date"])
        if entry["category"] not in ("markets", "data", "tools"):
            raise ValueError(f"Invalid category for {slug}")
        url = urlsplit(entry["source"])
        if url.scheme != "https" or not url.hostname or url.username or url.password:
            raise ValueError(f"Invalid source URL for {slug}")
        for locale in COPY:
            for field in ("title", "summary", "risk"):
                if not entry[locale][field].strip():
                    raise ValueError(f"Empty {field} for {slug} ({locale})")
    return sorted(notes, key=lambda note: note["date"], reverse=True)


def render_notes(notes, locale, copy):
    filters = copy["filters"]
    cards = []
    for entry in notes:
        slug = entry["id"]
        category = entry["category"]
        day = escape(entry["date"])
        source = escape(entry["source"], quote=True)
        note = {key: escape(value) for key, value in entry[locale].items()}
        cards.append(f"""
      <article class="note-card" id="{slug}" data-category="{category}">
        <div class="note-meta"><span>{filters[category]}</span><time datetime="{day}">{day}</time></div>
        <h3>{note["title"]}</h3>
        <p>{note["summary"]}</p>
        <p class="risk"><strong>{copy["risk"]}</strong> {note["risk"]}</p>
        <a class="text-link" href="{source}">{copy["source"]} <span aria-hidden="true">↗</span></a>
      </article>""")
    return "".join(cards)


def alpha(locale, root, notes, copy):
    questions = "".join(
        f"<li><strong>{label}</strong><span>{question}</span></li>"
        for label, question in copy["questions"]
    )
    filters = "\n".join(
        f'        <button type="button" data-filter="{key}" aria-pressed="{str(key == "all").lower()}">{label}</button>'
        for key, label in copy["filters"].items()
    )
    title_start, title_end = copy["title"]
    featured = ""
    if notes:
        latest = notes[0]
        title = escape(latest[locale]["title"])
        featured = f"""
        <a class="featured-note" href="#{latest["id"]}" data-show-note>
          <span class="featured-label">{copy["latest"]}</span>
          <strong>{title}</strong>
          <span class="featured-arrow" aria-hidden="true">↘</span>
        </a>"""
    empty_attr = " hidden" if notes else ""
    return f"""
    <section class="hero" aria-labelledby="title">
      <div class="hero-copy">
        <h1 id="title">{title_start} <span>{title_end}</span></h1>
        <p class="intro">{copy["intro"]}</p>
        <a class="primary" href="#feed">{copy["browse"]} <span aria-hidden="true">↓</span></a>
      </div>
      <div class="hero-feature">
        <div class="cover">
          <img src="{root}assets/refraction.webp" alt="" width="1440" height="960" fetchpriority="high">
        </div>{featured}
      </div>
    </section>
    <section class="section" id="feed" aria-labelledby="feed-title">
      <div class="section-header">
        <h2 id="feed-title">{copy["feed"]}</h2>
        <div id="filters" class="filters" role="group" aria-label="{copy["feed"]}" hidden>
{filters}
        </div>
      </div>
      <div id="notes" class="grid">{render_notes(notes, locale, copy)}
      </div>
      <p id="empty" class="empty"{empty_attr}>{copy["empty"]}</p>
    </section>
    <section class="method" aria-labelledby="method-title">
      <h2 id="method-title">{copy["method"]}</h2>
      <ol>{questions}</ol>
    </section>
    <aside class="share">
      <p>{copy["share"]}</p>
      <a class="text-link" href="mailto:{CONTACT}?subject=AlphaWink%20lead">{copy["send"]} <span aria-hidden="true">↗</span></a>
    </aside>
    <script src="{root}feed.js" defer></script>"""


def page_intro(title, intro, eyebrow, extra=""):
    return f"""
    <section class="page-intro" aria-labelledby="title">
      <p class="kicker">{eyebrow}</p>
      <h1 id="title">{title}</h1>
      <p class="intro">{intro}</p>
      {extra}
    </section>"""


def product_card(name, label, description, features, action):
    items = "".join(f"<li>{feature}</li>" for feature in features)
    return f"""
      <article class="product-card">
        <p class="kicker">{label}</p>
        <h2>{name}</h2>
        <p>{description}</p>
        <ul class="features">{items}</ul>
        <div class="product-action">{action}</div>
      </article>"""


def products(copy):
    source = f'<a class="text-link" href="{ALEPH}">{copy["source"]} <span aria-hidden="true">↗</span></a>'
    status = f'<span class="status">{copy["status"]}</span>'
    return page_intro(copy["title"], copy["intro"], "ALPHAWINK / PRODUCTS") + f"""
    <div class="grid product-grid">{product_card("AlephTX", *copy["aleph"], source)}
{product_card("Oasis Agent", *copy["oasis"], status)}
    </div>"""


def about(copy):
    github = f'<a class="text-link" href="{GITHUB}">{copy["github"]} <span aria-hidden="true">↗</span></a>'
    areas = "\n".join(
        f"      <article><h3>{title}</h3><p>{description}</p></article>"
        for title, description in copy["work_areas"]
    )
    stack = "".join(f"<div><dt>{area}</dt><dd>{tools}</dd></div>" for area, tools in copy["stack"])
    return page_intro(copy["title"], copy["intro"], "@VIMDAY", github) + f"""
    <section class="section work-section" aria-labelledby="work-title">
      <h2 id="work-title">{copy["work"]}</h2>
      <div class="grid work-grid">
{areas}
      </div>
    </section>
    <section class="section tool-section" aria-labelledby="tools-title">
      <h2 id="tools-title">{copy["tools"]}</h2>
      <dl class="tool-grid">{stack}</dl>
    </section>"""


def render(locale, page, notes):
    copy = COPY[locale]
    lang = "zh-Hans" if locale == "zh" else "en"
    route = ("zh/" if locale == "zh" else "") + ROUTES[page]
    root = "../" * route.count("/") or "./"
    here = root + ("zh/" if locale == "zh" else "")
    other_lang, other_label = ("en", "EN") if locale == "zh" else ("zh-Hans", "中文")
    other = root + ("zh/" if locale == "en" else "") + ROUTES[page]
    current = ' aria-current="page"'
    nav = "\n".join(
        f'      <a href="{here}{path}"{current if i == page else ""}>{copy["nav"][i]}</a>'
        for i, path in enumerate(ROUTES)
    )
    name = copy["nav"][page]
    section = copy[("alpha", "products", "about")[page]]
    if page == 0:
        body = alpha(locale, root, notes, section)
    elif page == 1:
        body = products(section)
    else:
        body = about(section)

    html = f"""<!-- Copyright 2025 vimday; SPDX-License-Identifier: Apache-2.0 -->
<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(section["intro"], quote=True)}">
  <meta name="theme-color" content="#f8f7f2">
  <title>AlphaWink · {name}</title>
  <link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{root}assets/site.css">
  <link rel="alternate" hreflang="{other_lang}" href="{other}">
</head>
<body>
  <a class="skip" href="#main">{copy["skip"]}</a>
  <header class="bar wrap">
    <a class="brand" href="{here}"><span aria-hidden="true">&gt;_</span> AlphaWink</a>
    <nav aria-label="{copy["nav_label"]}">
{nav}
      <a class="lang" href="{other}" lang="{other_lang}" hreflang="{other_lang}">{other_label}</a>
    </nav>
  </header>
  <main class="wrap" id="main">{body}
  </main>
  <footer class="wrap footer">
    <span>AlphaWink</span>
    <a href="mailto:{CONTACT}">{CONTACT}</a>
  </footer>
</body>
</html>
"""
    (ROOT / route / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    notes = read_notes()
    for locale in COPY:
        for page in range(len(ROUTES)):
            render(locale, page, notes)

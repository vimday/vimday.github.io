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
PROJECTS = (("aleph", "aleph-tx", "AlephTX"), ("oasis", "oasis-agent", "Oasis Agent"))

COPY = {
    "en": {
        "nav": ("Alpha", "Products", "About"),
        "skip": "Skip to content",
        "nav_label": "Site navigation",
        "alpha": {
            "title": ("Replay the", "market."),
            "intro": "AlphaWink studies market opportunities through recorded data, simulated execution, and decisions you can trace back to the evidence.",
            "browse": "Explore the projects",
            "read": "Read the notes",
            "projects": "Research projects",
            "feed": "Research notes",
            "filters": {"all": "All", "markets": "Market mechanics", "data": "Robotics data", "tools": "Research methods"},
            "empty": "No notes in this category yet.",
            "source": "Original source",
            "risk": "What to watch",
            "share": "Found something worth investigating?",
            "send": "Share a lead",
            "latest": "Latest note",
        },
        "products": {
            "title": "From market data to decisions",
            "intro": "AlephTX models how an idea might execute. Oasis Agent records how decisions were made and checks the limits for execution.",
            "aleph": (
                "Perpetual futures",
                "Replay both legs of a perpetual futures strategy against recorded market data.",
                "AlephTX combines recorded order-book depth, funding, and independent reference prices to study relative value across venues.",
                (
                    ("Build the dataset", "Align market depth, funding events, and reference prices."),
                    ("Replay execution", "Model order latency and partial fills across both legs."),
                    ("Read the costs", "Inspect simulated fills, fees, slippage, and settled funding."),
                ),
            ),
            "oasis": (
                "Evidence and risk",
                "Trace a strategy decision back to the observations and risk checks behind it.",
                "Oasis Agent records the inputs behind a strategy decision so researchers can replay it and examine the execution limits separately.",
                (
                    ("Keep the evidence", "Preserve the original observation, its source, and the state it came from."),
                    ("Replay the decision", "Revisit the decision and its accounting in simulation."),
                    ("Check the limits", "Evaluate exposure, loss limits, and authorization before execution."),
                ),
            ),
            "source": "View source on GitHub",
            "status": "In development",
        },
        "about": {
            "title": "Robotics data and AI infrastructure",
            "intro": "I build data platforms for embodied AI, including the workflows that turn multimodal robot data into datasets that teams can validate and reuse.",
            "github": "GitHub profile",
            "work": "Engineering work",
            "notes": "Engineering notes",
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
            "title": ("回放市场，", "检验假设。"),
            "intro": "AlphaWink 用市场记录和成交模拟研究机会，并保留决策依据，让每个判断都能回到原始证据。",
            "browse": "探索研究项目",
            "read": "阅读研究笔记",
            "projects": "研究项目",
            "feed": "研究笔记",
            "filters": {"all": "全部", "markets": "市场机制", "data": "机器人数据", "tools": "研究方法"},
            "empty": "这个分类还没有笔记。",
            "source": "原始来源",
            "risk": "需要留意",
            "share": "有值得研究的线索？",
            "send": "分享线索",
            "latest": "最新笔记",
        },
        "products": {
            "title": "从市场数据到决策",
            "intro": "AlephTX 模拟策略在市场中可能如何成交。Oasis Agent 记录决策过程，并检查执行边界。",
            "aleph": (
                "永续合约",
                "用历史盘口回放永续合约策略的两条腿。",
                "AlephTX 用记录下来的盘口深度、资金费率和独立参考价，研究不同市场之间的相对价值。",
                (
                    ("整理行情", "对齐盘口深度、资金费率结算事件和参考价格。"),
                    ("回放执行", "为策略的两条腿模拟订单延迟和部分成交。"),
                    ("拆解成本", "查看模拟成交、手续费、滑点和资金费收支。"),
                ),
            ),
            "oasis": (
                "证据与风控",
                "把策略判断追溯到当时的观察和风险检查。",
                "Oasis Agent 保存策略判断的输入，让研究者能回放决策，并独立检查执行的风险边界。",
                (
                    ("保留证据", "记录原始观察、数据来源和观察对应的状态。"),
                    ("回放判断", "在模拟环境中复查决策和记账过程。"),
                    ("检查边界", "在执行前检查敞口、亏损上限和授权范围。"),
                ),
            ),
            "source": "在 GitHub 查看源码",
            "status": "开发中",
        },
        "about": {
            "title": "机器人数据与 AI 基础设施",
            "intro": "我做具身智能数据平台和 AI 基础设施，把多模态机器人数据处理成可校验、可复用的数据集。",
            "github": "GitHub 主页",
            "work": "工程经历",
            "notes": "工程笔记",
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


def project_previews(here, copy):
    previews = []
    for key, slug, name in PROJECTS:
        label, summary, _, _ = copy[key]
        previews.append(f"""
      <a class="project-preview" href="{here}products/#{slug}" aria-labelledby="preview-{slug}">
        <p class="kicker">{label}</p>
        <h3 id="preview-{slug}">{name}</h3>
        <p class="preview-summary">{summary}</p>
        <span class="preview-arrow" aria-hidden="true">↗</span>
      </a>""")
    return "".join(previews)


def alpha(locale, root, here, notes, copy, products_copy):
    categories = {entry["category"] for entry in notes}
    filters = "\n".join(
        f'        <button type="button" data-filter="{key}" aria-pressed="{str(key == "all").lower()}">{label}</button>'
        for key, label in copy["filters"].items()
        if key == "all" or key in categories
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
        <div class="hero-actions">
          <a class="primary" href="#research-projects">{copy["browse"]} <span aria-hidden="true">↓</span></a>
          <a class="text-link" href="#feed">{copy["read"]}</a>
        </div>
      </div>
      <div class="hero-feature">
        <div class="cover">
          <img src="{root}assets/market-pulse.webp" alt="" width="1440" height="960" fetchpriority="high">
        </div>{featured}
      </div>
    </section>
    <section class="section showcase" id="research-projects" aria-labelledby="projects-title">
      <h2 id="projects-title">{copy["projects"]}</h2>
      <div class="grid project-previews">{project_previews(here, products_copy)}
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


def product_card(slug, name, label, _summary, description, steps, action):
    workflow = "".join(
        f"<div><dt>{step}</dt><dd>{detail}</dd></div>" for step, detail in steps
    )
    return f"""
      <article class="product-card" id="{slug}">
        <p class="kicker">{label}</p>
        <h2>{name}</h2>
        <p>{description}</p>
        <dl class="product-workflow">{workflow}</dl>
        <div class="product-action">{action}</div>
      </article>"""


def products(copy):
    source = f'<a class="text-link" href="{ALEPH}">{copy["source"]} <span aria-hidden="true">↗</span></a>'
    status = f'<span class="status">{copy["status"]}</span>'
    actions = {"aleph": source, "oasis": status}
    cards = "".join(
        product_card(slug, name, *copy[key], actions[key])
        for key, slug, name in PROJECTS
    )
    return page_intro(copy["title"], copy["intro"], "ALPHAWINK / PRODUCTS") + f"""
    <div class="grid product-grid">{cards}
    </div>"""


def about(locale, notes, copy, notes_copy):
    github = f'<a class="text-link" href="{GITHUB}">{copy["github"]} <span aria-hidden="true">↗</span></a>'
    areas = "\n".join(
        f"      <article><h3>{title}</h3><p>{description}</p></article>"
        for title, description in copy["work_areas"]
    )
    stack = "".join(f"<div><dt>{area}</dt><dd>{tools}</dd></div>" for area, tools in copy["stack"])
    archive = ""
    if notes:
        archive = f"""
    <section class="section archive-section" aria-labelledby="archive-title">
      <h2 id="archive-title">{copy["notes"]}</h2>
      <div class="grid archive-grid">{render_notes(notes, locale, notes_copy)}
      </div>
    </section>"""
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
    </section>{archive}"""


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
        market_notes = [note for note in notes if note["category"] != "data"]
        body = alpha(locale, root, here, market_notes, section, copy["products"])
    elif page == 1:
        body = products(section)
    else:
        engineering_notes = [note for note in notes if note["category"] == "data"]
        body = about(locale, engineering_notes, section, copy["alpha"])

    html = f"""<!-- Copyright 2025 vimday; SPDX-License-Identifier: Apache-2.0 -->
<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(section["intro"], quote=True)}">
  <meta name="theme-color" content="#10100f">
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

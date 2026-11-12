"""Build the English and Simplified Chinese pages."""

import json
import re
from datetime import date
from hashlib import sha256
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CONTACT = "hi@alphawink.com"
GITHUB = "https://github.com/vimday"
ALEPH = "https://github.com/AlephTX/aleph-tx"
ROUTES = ("", "products/", "about/")
PROJECTS = (("aleph", "aleph-tx", "AlephTX"), ("oasis", "oasis-agent", "Oasis Agent"))
REPLAY_OFFSETS_MS = (0, 240, 480)
ASSETS = {
    path: f"{path}?v={sha256((ROOT / path).read_bytes()).hexdigest()[:10]}"
    for path in ("assets/site.css", "feed.js")
}

COPY = {
    "en": {
        "nav": ("Alpha", "Products", "About"),
        "skip": "Skip to content",
        "nav_label": "Site navigation",
        "alpha": {
            "title": "Independent market research",
            "intro": "We study market opportunities with recorded data and simulated trades.",
            "projects": "Research projects",
            "feed": "Research notes",
            "filters": {"all": "All", "markets": "Market mechanics", "data": "Robotics data", "tools": "Research methods"},
            "empty": "No notes in this category yet.",
            "source": "Original source",
            "risk": "What to watch",
        },
        "products": {
            "title": "From market data to decisions",
            "intro": "AlephTX models how an idea might execute. Oasis Agent records how decisions were made and checks the limits for execution.",
            "example": "Illustrative replay",
            "timeline": "Replay timeline",
            "play": "Play",
            "pause": "Pause",
            "replay": {
                "aleph": (
                    (("Venue A ask", "100.04"), ("Venue B bid", "100.07"), ("Available size", "2.00")),
                    (("A · simulated buy", "100.05"), ("B · simulated sell", "100.06"), ("Matched size", "1.50")),
                    (("Fees · quote units", "0.06"), ("Slippage · quote units", "0.03"), ("Funding · quote units", "0.00")),
                ),
                "oasis": (
                    (("Source", "Order books"), ("Observed spread", "0.03"), ("Record", "Snapshot")),
                    (("Mode", "Simulation"), ("Requested size", "2.00"), ("Matched size", "1.50")),
                    (("Exposure / limit", "1.50 / 2.00"), ("Loss limit", "Within limit"), ("Authorization", "Review required")),
                ),
            },
            "aleph": (
                "Perpetual futures",
                "AlephTX combines recorded order-book depth, funding, and independent reference prices to study relative value across venues.",
                (
                    ("Build the dataset", "Align market depth, funding events, and reference prices."),
                    ("Replay execution", "Model order latency and partial fills across both legs."),
                    ("Read the costs", "Inspect simulated fills, fees, slippage, and settled funding."),
                ),
            ),
            "oasis": (
                "Evidence and risk",
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
            "title": "独立市场研究",
            "intro": "从盘口、成交与风险出发，研究市场机会。",
            "projects": "研究项目",
            "feed": "研究笔记",
            "filters": {"all": "全部", "markets": "市场机制", "data": "机器人数据", "tools": "研究方法"},
            "empty": "这个分类还没有笔记。",
            "source": "原始来源",
            "risk": "需要留意",
        },
        "products": {
            "title": "从市场数据到决策",
            "intro": "AlephTX 模拟策略在市场中可能如何成交。Oasis Agent 记录决策过程，并检查执行边界。",
            "example": "示例回放",
            "timeline": "回放时间轴",
            "play": "播放",
            "pause": "暂停",
            "replay": {
                "aleph": (
                    (("A 市场卖一价", "100.04"), ("B 市场买一价", "100.07"), ("可用数量", "2.00")),
                    (("A 市场模拟买入价", "100.05"), ("B 市场模拟卖出价", "100.06"), ("双边成交量", "1.50")),
                    (("手续费 · 计价单位", "0.06"), ("滑点 · 计价单位", "0.03"), ("资金费 · 计价单位", "0.00")),
                ),
                "oasis": (
                    (("来源", "盘口"), ("观察到的价差", "0.03"), ("记录", "快照")),
                    (("运行模式", "模拟"), ("委托数量", "2.00"), ("双边成交量", "1.50")),
                    (("敞口 / 上限", "1.50 / 2.00"), ("亏损检查", "限额内"), ("执行授权", "待审核")),
                ),
            },
            "aleph": (
                "永续合约",
                "AlephTX 用记录下来的盘口深度、资金费率和独立参考价，研究不同市场之间的相对价值。",
                (
                    ("整理行情", "对齐盘口深度、资金费率结算事件和参考价格。"),
                    ("回放执行", "为策略的两条腿模拟订单延迟和部分成交。"),
                    ("拆解成本", "查看模拟成交、手续费、滑点和资金费收支。"),
                ),
            ),
            "oasis": (
                "证据与风控",
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
            "title": '机器人数据与 <span class="phrase">AI 基础设施</span>',
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
        <div class="note-meta"><time datetime="{day}">{day}</time><span>{filters[category]}</span></div>
        <div class="note-content">
          <h3>{note["title"]}</h3>
          <p>{note["summary"]}</p>
          <p class="risk"><strong>{copy["risk"]}</strong> {note["risk"]}</p>
          <a class="text-link" href="{source}">{copy["source"]} <span aria-hidden="true">↗</span></a>
        </div>
      </article>""")
    return "".join(cards)


def product_replay(copy, workflow, examples):
    ticks = "".join(f"<span>{offset} ms</span>" for offset in REPLAY_OFFSETS_MS)
    frames = []
    for (title, detail), offset, values in zip(workflow, REPLAY_OFFSETS_MS, examples, strict=True):
        metrics = "".join(f"<div><dt>{label}</dt><dd>{value}</dd></div>" for label, value in values)
        frames.append(f"""
          <div class="replay-frame" data-frame>
            <div class="frame-copy">
              <p class="frame-time">00:00.{offset:03d}</p>
              <h3>{title}</h3>
              <p>{detail}</p>
            </div>
            <dl class="frame-metrics">{metrics}</dl>
          </div>""")
    return f"""
        <details class="replay" name="project-replay" data-replay>
          <summary>{copy["example"]}</summary>
          <div class="replay-frames">{"".join(frames)}
          </div>
          <div class="replay-controls" data-replay-controls hidden>
            <button class="replay-play" type="button" data-play="{copy["play"]}" data-pause="{copy["pause"]}">
              <span class="play-icon" aria-hidden="true"></span><span>{copy["play"]}</span>
            </button>
            <div class="replay-track">
              <input type="range" min="0" max="{len(REPLAY_OFFSETS_MS) - 1}" step="1" value="0" aria-label="{copy["timeline"]}">
              <div class="replay-ticks" aria-hidden="true">{ticks}</div>
            </div>
          </div>
        </details>"""


def alpha(locale, root, here, notes, copy):
    categories = {entry["category"] for entry in notes}
    filters = "\n".join(
        f'        <button type="button" data-filter="{key}" aria-pressed="{str(key == "all").lower()}">{label}</button>'
        for key, label in copy["filters"].items()
        if key == "all" or key in categories
    )
    projects = "".join(
        f'<a class="text-link" href="{here}products/#{slug}">{name} <span aria-hidden="true">↗</span></a>'
        for _, slug, name in PROJECTS
    )
    empty_attr = " hidden" if notes else ""
    return page_intro(copy["title"], copy["intro"]) + f"""
    <section class="section" id="feed" aria-labelledby="feed-title">
      <div class="section-header">
        <h2 id="feed-title">{copy["feed"]}</h2>
        <div id="filters" class="filters" role="group" aria-label="{copy["feed"]}" hidden>
{filters}
        </div>
      </div>
      <div id="notes" class="note-index">{render_notes(notes, locale, copy)}
      </div>
      <p id="empty" class="empty"{empty_attr}>{copy["empty"]}</p>
    </section>
    <section class="project-index" id="research-walkthrough" aria-labelledby="research-projects">
      <h2 id="research-projects">{copy["projects"]}</h2>
      <div>{projects}</div>
    </section>
    <script src="{root}{ASSETS["feed.js"]}" defer></script>"""


def page_intro(title, intro, eyebrow="", extra=""):
    label = f'<p class="kicker">{eyebrow}</p>' if eyebrow else ""
    return f"""
    <section class="page-intro" aria-labelledby="title">
      {label}
      <h1 id="title">{title}</h1>
      <p class="intro">{intro}</p>
      {extra}
    </section>"""


def product_card(slug, name, label, description, replay, action):
    return f"""
      <article class="product" id="{slug}">
        <div class="product-title">
          <p class="kicker">{label}</p>
          <h2>{name}</h2>
        </div>
        <div class="product-content">
          <p>{description}</p>
          <div class="product-action">{action}</div>{replay}
        </div>
      </article>"""


def products(root, copy):
    source = f'<a class="text-link" href="{ALEPH}">{copy["source"]} <span aria-hidden="true">↗</span></a>'
    status = copy["status"]
    actions = {"aleph": source, "oasis": status}
    cards = []
    for key, slug, name in PROJECTS:
        label, description, workflow = copy[key]
        replay = product_replay(copy, workflow, copy["replay"][key])
        cards.append(product_card(slug, name, label, description, replay, actions[key]))
    return page_intro(copy["title"], copy["intro"]) + f"""
    <div class="product-list" id="research-walkthrough">{"".join(cards)}
    </div>
    <script src="{root}{ASSETS["feed.js"]}" defer></script>"""


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
      <div class="archive-grid">{render_notes(notes, locale, notes_copy)}
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
        body = alpha(locale, root, here, market_notes, section)
    elif page == 1:
        body = products(root, section)
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
  <meta name="theme-color" content="#faf9f6">
  <title>AlphaWink · {name}</title>
  <link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{root}{ASSETS["assets/site.css"]}">
  <link rel="alternate" hreflang="{other_lang}" href="{other}">
</head>
<body>
  <a class="skip" href="#main">{copy["skip"]}</a>
  <header class="bar wrap">
    <a class="brand" href="{here}">AlphaWink</a>
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

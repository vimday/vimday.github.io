"""Build the English and Simplified Chinese pages."""

import json
import re
from datetime import date
from decimal import Decimal
from hashlib import sha256
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
REPORT_CONTENT = ROOT / "content" / "research"
CONTACT = "hi@alphawink.com"
GITHUB = "https://github.com/vimday"
ROUTES = ("", "products/", "about/")
NAV_ROUTES = ("", "research/", "products/", "about/")
PROJECTS = (
    ("aleph", "aleph-tx", "AlephTX", "https://github.com/AlephTX/aleph-tx",
     "blob/main/docs/QUICKSTART.md", "commit/5fe4251ce09341c6a6148571ab5b8606065db928", "blob/main/docs/CROSS_VENUE.md"),
    ("oasis", "oasis-agent", "Oasis Agent", "https://github.com/vimday/oasis-agent",
     "#quickstart", "commit/13acce072dfdfeb98e0cb2b0ad5af55308df997d", "blob/main/docs/CURRENT_IMPLEMENTATION.md"),
)
ASSETS = {
    path: f"{path}?v={sha256((ROOT / path).read_bytes()).hexdigest()[:10]}"
    for path in (
        "assets/site.css",
        "feed.js",
        "favicon.svg",
        "favicon.ico",
        "favicon-32x32.png",
        "favicon-96x96.png",
        "apple-touch-icon.png",
    )
}

COPY = {
    "en": {
        "nav": ("Home", "Research", "Products", "About"),
        "skip": "Skip to content",
        "nav_label": "Site navigation",
        "research": {
            "heading": "Latest research",
            "archive": "Research archive",
            "archive_intro": "Investigations into trading, market structure and risk.",
            "back": "All research",
            "read": "Read the report",
            "updated": "Updated",
            "contents": "In this report",
            "moved": "This report is now part of the full investigation.",
        },
        "alpha": {
            "title": "Independent <span>market research</span>",
            "intro": "We study how markets trade, what execution costs, and where risk sits. Our research and code are public.",
            "browse": "Explore research",
            "receipt": {
                "block": "Ethereum block",
                "net": "Wallet net increase",
                "builder": "Builder payment",
                "gas": "Gas",
                "trace": "Read the transaction analysis",
            },
            "projects": "Research systems",
            "feed": "Research notes",
            "filters": {"all": "All", "markets": "Market mechanics", "data": "Robotics data", "tools": "Research methods"},
            "empty": "No notes in this category yet.",
            "source": "Original source",
            "risk": "What to watch",
        },
        "products": {
            "title": "Systems for market research",
            "intro": "AlephTX records and replays how perpetual markets trade. Oasis Agent reconstructs on-chain decisions from evidence and applies independent risk checks before execution.",
            "source": "View on GitHub",
            "start": "Quickstart",
            "changes": "Recent work",
            "commit": "View change",
            "browse": "Explore products",
            "aleph": {
                "topic": "Perpetual futures",
                "summary": "Multi-venue order books, causal replay and supervised execution in Rust and Go.",
                "detail": "AlephTX links three workflows. Its Go feeder and Rust strategy engine share a versioned market-data interface. A separate capture pipeline retains the data for replay, so research can evaluate a decision using the information available at the time.",
                "status": "MIT licensed",
                "docs": "Venue and replay guide",
                "capabilities": (
                    ("Record", "Capture depth, public trades and funding, with independent reference prices and sealed archive segments."),
                    ("Replay", "Compile events in arrival order, model the fills on each leg and attribute fees, funding and post-fill markouts."),
                    ("Execute with supervision", "Track orders and journal recovery. Maker, cancel and taker lanes use separate signing credentials and nonce tracking."),
                ),
                "scope": "The supervised mode supports Lighter market making and a separately gated Hyperliquid hedge. Paper trading keeps quantitative profit, hedge arbitrage and incentive turnover in separate ledgers.",
                "recent": "The market-making replay now captures common price shocks across venues, recovery and attribution for risk-reducing bids.",
            },
            "oasis": {
                "topic": "On-chain evidence and risk",
                "summary": "Block-pinned research, deterministic replay and execution with independently enforced limits.",
                "detail": "Oasis Agent retains raw observations and ties them to a chain, block hash and input configuration. It reconciles strategy decisions with balances and receipts. Loss, exposure and transaction-scope checks run independently of the strategy.",
                "status": "Public repository",
                "docs": "Verified capabilities",
                "capabilities": (
                    ("Reconstruct evidence", "Retain the provider response and replay from pinned state, including the exact pre-transaction state when available."),
                    ("Run in shadow", "Review Uniswap v4 liquidity provision, Base spot paper positions and multihop swap research on retained inputs."),
                    ("Gate execution", "Live canaries require explicit authorization and run within configured bounds. Journals preserve receipts, recovery and STOP state."),
                ),
                "scope": "The quickstart runs an offline benchmark. The project also documents a bounded Base LP canary and a Base spot shadow ledger. Each new live run requires fresh evidence and approval.",
                "recent": "Recent research work replays historical multihop swaps from the exact pre-transaction state. The capability index links the evidence and the conditions of each result.",
            },
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
        "nav": ("首页", "研究", "产品", "关于"),
        "skip": "跳到正文",
        "nav_label": "网站导航",
        "research": {
            "heading": "最新研究",
            "archive": "研究归档",
            "archive_intro": "关于交易、市场结构和风险的深度研究。",
            "back": "全部研究",
            "read": "阅读全文",
            "updated": "更新于",
            "contents": "本文目录",
            "moved": "这篇报告已并入完整研究。",
        },
        "alpha": {
            "title": "独立市场研究",
            "intro": '研究成交、成本与风险。我们公开研究文章和验证这些判断的代码。',
            "browse": "浏览研究",
            "receipt": {
                "block": "以太坊区块",
                "net": "发起钱包净增",
                "builder": "构建者付款",
                "gas": "Gas",
                "trace": "阅读交易复盘",
            },
            "projects": "研究系统",
            "feed": "研究笔记",
            "filters": {"all": "全部", "markets": "市场机制", "data": "机器人数据", "tools": "研究方法"},
            "empty": "这个分类还没有笔记。",
            "source": "原始来源",
            "risk": "需要留意",
        },
        "products": {
            "title": "为市场研究构建的系统",
            "intro": "AlephTX 记录并回放永续合约市场。Oasis Agent 用原始证据复盘链上决策，在执行前独立校验风险。",
            "source": "GitHub 源码",
            "start": "快速开始",
            "changes": "近期更新",
            "commit": "查看提交",
            "browse": "查看产品",
            "aleph": {
                "topic": "永续合约",
                "summary": "跨平台订单簿、因果回放与受监督执行，核心由 Rust 和 Go 实现。",
                "detail": "AlephTX 将采集、研究与执行连起来。Go 行情进程和 Rust 策略引擎通过版本化的共享内存接口交换数据，独立采集链路保存回放材料，让研究能按决策当时可见的信息检验策略。",
                "status": "MIT 许可",
                "docs": "平台与回放文档",
                "capabilities": (
                    ("采集", "连续采集盘口深度、公开成交与资金费率，保留独立参考价，为归档分段做校验。"),
                    ("回放", "按数据实际到达顺序重放，建模两腿成交，再核算手续费、资金费与成交后的价格偏移。"),
                    ("受监督执行", "追踪订单与恢复日志。挂单、撤单和吃单使用分离的签名密钥与 nonce 跟踪。"),
                ),
                "scope": "受监督模式支持 Lighter 做市，Hyperliquid 对冲单独授权。纸面研究将量化收益、对冲套利与激励周转分别记账。",
                "recent": "做市回放新增跨市场共同价格冲击的触发与恢复判断，并为降低敞口的买单补上成交归因。",
            },
            "oasis": {
                "topic": "链上证据与风控",
                "summary": "固定区块状态的研究、可复现回放，以及由独立风控限制的执行。",
                "detail": "Oasis Agent 保留原始观测，将它与链、区块哈希和输入配置绑定，再用余额和回执核对策略决策。亏损、敞口和交易权限由策略之外的风控层校验。",
                "status": "公开仓库",
                "docs": "已验证的能力",
                "capabilities": (
                    ("还原证据", "保留数据源的原始响应，按固定状态回放。有条件时精确恢复交易前状态。"),
                    ("影子验证", "用留存输入研究 Uniswap v4 流动性、Base 现货纸面仓位与多跳兑换。"),
                    ("审核后执行", "实盘小范围验证要求明确授权，按配置限制执行。日志保留回执、恢复记录和停止状态。"),
                ),
                "scope": "快速开始可以离线运行基准案例。仓库也公开了 Base LP 的小范围实盘验证和 Base 现货影子账本。新一轮实盘仍需当期证据与授权。",
                "recent": "近期新增了从精确交易前状态回放历史多跳兑换。能力索引列出各项结论对应的证据和适用条件。",
            },
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


def read_reports():
    reports = json.loads((REPORT_CONTENT / "index.json").read_text(encoding="utf-8"))
    ids = set()
    for report in reports:
        slug = report["id"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or slug in ids:
            raise ValueError(f"Invalid or duplicate report ID: {slug}")
        ids.add(slug)
        published = date.fromisoformat(report["date"])
        if "updated" in report and date.fromisoformat(report["updated"]) < published:
            raise ValueError(f"Update precedes publication: {slug}")
        for locale in COPY:
            for field in ("title", "summary", "topic"):
                if not report[locale][field].strip():
                    raise ValueError(f"Empty {field} for {slug} ({locale})")
    for report in reports:
        if "redirect" in report:
            previous = report["redirect"]["from"]
            if previous in ids or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", previous):
                raise ValueError(f'Invalid previous report ID: {previous}')
            ids.add(previous)
    return sorted(reports, key=lambda report: report["date"], reverse=True)


def report_path(report):
    return f'research/{report["id"]}/'


def featured_receipt(report, copy, here):
    receipt = report["receipt"]
    amounts = {key: Decimal(receipt[key]) for key in ("net", "builder", "gas")}
    if any(not value.is_finite() or value < 0 for value in amounts.values()) or not (total := sum(amounts.values())):
        raise ValueError(f'Invalid receipt amounts for {report["id"]}')
    asset = escape(receipt["asset"])
    widths = "".join(f'<span style="flex-grow:{value / total:.7f}"></span>' for value in amounts.values())
    costs = "".join(f'<div><dt>{copy[key]}</dt><dd>{amounts[key]:f} {asset}</dd></div>'
                    for key in ("builder", "gas"))
    return f"""
      <figure class="hero-receipt">
        <figcaption>
          <strong>{escape(receipt["market"])}</strong>
          <span>{copy["block"]} {receipt["block"]:,}</span>
        </figcaption>
        <dl class="receipt-data">
          <div class="receipt-net">
            <dt>{copy["net"]}</dt>
            <dd>{amounts["net"]:f} <span>{asset}</span></dd>
          </div>
          {costs}
        </dl>
        <div class="receipt-bar" aria-hidden="true">{widths}</div>
        <a class="receipt-link" href="{here}{report_path(report)}#cost">{copy["trace"]} <span aria-hidden="true">↗</span></a>
      </figure>"""


def home_intro(reports, copy, here):
    lead = reports[0] if reports else None
    receipt = featured_receipt(lead, copy["receipt"], here) if lead and "receipt" in lead else ""
    return f"""
    <section class="home-hero{' home-hero-receipt' if receipt else ''}" aria-labelledby="title">
      <div class="hero-copy">
        <h1 id="title">{copy["title"]}</h1>
        <p>{copy["intro"]}</p>
        <a class="hero-link" href="{here}research/">{copy["browse"]} <span aria-hidden="true">↗</span></a>
      </div>{receipt}
    </section>"""


def report_meta(report, locale):
    topic = escape(report[locale]["topic"])
    day = report["date"]
    return f'<div class="report-meta"><span>{topic}</span><time datetime="{day}">{day}</time></div>'


def report_entry(report, locale, here, *, heading="h3", featured=False):
    fields = report[locale]
    url = here + report_path(report)
    label = COPY[locale]["research"]["read"]
    action = f'<a class="text-link" href="{url}" aria-label="{label} · {escape(fields["title"], quote=True)}">{label} <span aria-hidden="true">→</span></a>' if featured else ""
    return f"""
        <article class="report-entry{' report-feature' if featured else ''}">
          {report_meta(report, locale)}
          <{heading}><a href="{url}">{escape(fields["title"])}</a></{heading}>
          <p>{escape(fields["summary"])}</p>
          {action}
        </article>"""


def latest_research(reports, locale, here):
    if not reports:
        return ""
    copy = COPY[locale]["research"]
    lead = report_entry(reports[0], locale, here, featured=True)
    more = "".join(report_entry(report, locale, here) for report in reports[1:4])
    return f"""
    <section class="section" id="reports" aria-labelledby="reports-title">
      <div class="section-header">
        <h2 id="reports-title">{copy["heading"]}</h2>
        <a class="text-link" href="{here}research/">{copy["back"]} <span aria-hidden="true">→</span></a>
      </div>
      <div class="research-front">
        {lead}
        <div class="research-front-list">{more}
        </div>
      </div>
    </section>"""


def research_archive(reports, locale):
    copy = COPY[locale]["research"]
    here = "/zh/" if locale == "zh" else "/"
    entries = "".join(report_entry(report, locale, here, heading="h2") for report in reports)
    return page_intro(copy["archive"], copy["archive_intro"]) + f'<div class="research-archive">{entries}</div>'


def report_body(report, locale):
    copy = COPY[locale]["research"]
    fields = report[locale]
    body = (REPORT_CONTENT / report["id"] / f"{locale}.html").read_text(encoding="utf-8")
    headings = re.findall(r'<h2 id="([a-z0-9-]+)">([^<]+)</h2>', body)
    anchors = dict(headings)
    if "redirect" in report and report["redirect"]["section"] not in anchors:
        raise ValueError(f'Missing redirect heading for {report["id"]} ({locale})')
    if "receipt" in report and "cost" not in anchors:
        raise ValueError(f'Missing receipt cost heading for {report["id"]} ({locale})')
    contents = "".join(f'<li><a href="#{anchor}">{title}</a></li>' for anchor, title in headings)
    updated = ""
    if "updated" in report:
        day = report["updated"]
        updated = f'<p class="report-updated">{copy["updated"]} <time datetime="{day}">{day}</time></p>'
    return f"""
    <article class="report" aria-labelledby="title">
      <div class="reading-progress" aria-hidden="true"></div>
      <header class="report-intro">
        <a class="text-link report-back" href="../"><span aria-hidden="true">←</span> {copy["back"]}</a>
        {report_meta(report, locale)}
        <h1 id="title">{escape(fields["title"])}</h1>
        <p class="report-deck">{escape(fields["summary"])}</p>{updated}
      </header>
      <div class="report-layout">
        <nav class="report-toc" aria-labelledby="contents-title">
          <p id="contents-title">{copy["contents"]}</p>
          <ul>{contents}</ul>
        </nav>
        <div class="report-prose">
{body}
          <div class="report-end"><a class="text-link" href="../"><span aria-hidden="true">←</span> {copy["back"]}</a></div>
        </div>
      </div>
    </article>"""


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


def project_index(locale, here, title):
    copy = COPY[locale]["products"]
    entries = "".join(
        f'<article><h3><a href="{here}products/#{slug}">{name} <span aria-hidden="true">↗</span></a></h3>'
        f'<p>{escape(copy[key]["summary"])}</p></article>'
        for key, slug, name, *_ in PROJECTS
    )
    return f"""
    <section class="section project-index" id="research-walkthrough" aria-labelledby="research-projects">
      <div class="section-header">
        <h2 id="research-projects">{title}</h2>
        <a class="text-link" href="{here}products/">{copy["browse"]} <span aria-hidden="true">→</span></a>
      </div>
      <div class="project-index-grid">{entries}</div>
    </section>"""


def alpha(locale, root, here, notes, reports, copy):
    categories = {entry["category"] for entry in notes}
    filters = "\n".join(
        f'        <button type="button" data-filter="{key}" aria-pressed="{str(key == "all").lower()}">{label}</button>'
        for key, label in copy["filters"].items()
        if key == "all" or key in categories
    )
    empty_attr = " hidden" if notes else ""
    return home_intro(reports, copy, here) + f"""
{latest_research(reports, locale, here)}
{project_index(locale, here, copy["projects"])}
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
    <script src="{root}{ASSETS["feed.js"]}" defer></script>"""


def page_intro(title, intro, eyebrow="", extra="", *, masthead=False):
    label = f'<p class="kicker">{eyebrow}</p>' if eyebrow else ""
    classes = "page-intro masthead" if masthead else "page-intro"
    return f"""
    <section class="{classes}" aria-labelledby="title">
      {label}
      <h1 id="title">{title}</h1>
      <p class="intro">{intro}</p>
      {extra}
    </section>"""


def products(copy):
    cards = []
    for key, slug, name, repo, start, recent, docs in PROJECTS:
        fields = copy[key]
        quickstart = repo + start if start.startswith("#") else f"{repo}/{start}"
        capabilities = "".join(
            f"<div><dt>{escape(title)}</dt><dd>{escape(detail)}</dd></div>"
            for title, detail in fields["capabilities"]
        )
        cards.append(f"""
      <article class="product" id="{slug}" aria-labelledby="{slug}-title">
        <header class="product-heading">
          <p class="kicker">{fields["topic"]} <span aria-hidden="true">·</span> {fields["status"]}</p>
          <h2 id="{slug}-title">{name}</h2>
          <p>{escape(fields["summary"])}</p>
          <div class="product-actions">
            <a class="product-source" href="{repo}" aria-label="{copy["source"]} · {name}">{copy["source"]} <span aria-hidden="true">↗</span></a>
            <a class="text-link" href="{quickstart}">{copy["start"]}</a>
          </div>
        </header>
        <div class="product-content">
          <p>{escape(fields["detail"])}</p>
          <dl class="product-capabilities">{capabilities}</dl>
          <p class="product-scope">{escape(fields["scope"])}</p>
          <div class="product-update">
            <h3>{copy["changes"]}</h3>
            <p>{escape(fields["recent"])}</p>
            <div class="product-docs">
              <a class="text-link" href="{repo}/{recent}">{copy["commit"]} <span aria-hidden="true">↗</span></a>
              <a class="text-link" href="{repo}/{docs}">{fields["docs"]} <span aria-hidden="true">↗</span></a>
            </div>
          </div>
        </div>
      </article>""")
    names = "".join(f'<a class="text-link" href="#{slug}">{name} <span aria-hidden="true">↓</span></a>'
                    for _, slug, name, *_ in PROJECTS)
    return page_intro(copy["title"], copy["intro"], masthead=True) + f"""
    <div class="product-jump">{names}</div>
    <div class="product-list" id="research-walkthrough">{"".join(cards)}
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


def render(locale, page, notes, reports):
    copy = COPY[locale]
    path = ROUTES[page]
    name = copy["nav"][NAV_ROUTES.index(path)]
    section = copy[("alpha", "products", "about")[page]]
    description = re.sub(r"<[^>]+>", "", section["intro"])
    root = "../" * (path.count("/") + (locale == "zh")) or "./"
    here = root + ("zh/" if locale == "zh" else "")
    if page == 0:
        market_notes = [note for note in notes if note["category"] != "data"]
        body = alpha(locale, root, here, market_notes, reports, section)
    elif page == 1:
        body = products(section)
    else:
        engineering_notes = [note for note in notes if note["category"] == "data"]
        body = about(locale, engineering_notes, section, copy["alpha"])
    write_page(locale, path, name, description, body)


def write_page(locale, path, name, description, body, *, redirect=None):
    copy = COPY[locale]
    lang = "zh-Hans" if locale == "zh" else "en"
    route = ("zh/" if locale == "zh" else "") + path
    root = "../" * route.count("/") or "./"
    mark = root + ASSETS["favicon.svg"]
    here = root + ("zh/" if locale == "zh" else "")
    other_lang, other_label = ("en", "English") if locale == "zh" else ("zh-Hans", "中文")
    other = root + ("zh/" if locale == "en" else "") + path
    current = {path: ' aria-current="page"'}
    if path.startswith("research/") and path != "research/":
        current["research/"] = ' aria-current="location"'
    nav = "\n".join(
        f'      <a href="{here}{nav_path}"{current.get(nav_path, "")}>{label}</a>'
        for nav_path, label in zip(NAV_ROUTES, copy["nav"], strict=True)
    )
    redirect_head = ""
    if redirect:
        target = escape(redirect, quote=True)
        redirect_head = f'\n  <meta http-equiv="refresh" content="0; url={target}">\n  <link rel="canonical" href="{target.split("#", 1)[0]}">'
    html = f"""<!-- Copyright 2025 vimday; SPDX-License-Identifier: Apache-2.0 -->
<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(description, quote=True)}">
  <meta name="theme-color" content="#f5f5f5">
  <title>{escape(name)} / AlphaWink</title>
  <link rel="icon" href="{root}{ASSETS["favicon.ico"]}" sizes="16x16 32x32 48x48" type="image/x-icon">
  <link rel="icon" href="{root}{ASSETS["favicon-32x32.png"]}" sizes="32x32" type="image/png">
  <link rel="icon" href="{root}{ASSETS["favicon-96x96.png"]}" sizes="96x96" type="image/png">
  <link rel="apple-touch-icon" href="{root}{ASSETS["apple-touch-icon.png"]}" sizes="180x180">
  <link rel="stylesheet" href="{root}{ASSETS["assets/site.css"]}">
  <link rel="alternate" hreflang="{other_lang}" href="{other}">{redirect_head}
</head>
<body>
  <a class="skip" href="#main">{copy["skip"]}</a>
  <header class="bar wrap">
    <a class="brand" href="{here}" aria-label="AlphaWink">
      <img class="brand-mark" src="{mark}" alt="" width="28" height="28">
      <span class="brand-name">AlphaWink</span>
    </a>
    <nav aria-label="{copy["nav_label"]}">
{nav}
    </nav>
  </header>
  <main class="wrap" id="main">{body}
  </main>
  <footer class="wrap footer">
    <span>AlphaWink</span>
    <div class="footer-links">
      <a href="mailto:{CONTACT}">{CONTACT}</a>
      <a href="{other}" lang="{other_lang}" hreflang="{other_lang}">{other_label}</a>
    </div>
  </footer>
</body>
</html>
"""
    destination = ROOT / route
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    notes = read_notes()
    reports = read_reports()
    for locale in COPY:
        for page in range(len(ROUTES)):
            render(locale, page, notes, reports)
        archive = COPY[locale]["research"]
        write_page(locale, "research/", archive["archive"], archive["archive_intro"], research_archive(reports, locale))
        for report in reports:
            fields = report[locale]
            write_page(locale, report_path(report), fields["title"], fields["summary"], report_body(report, locale))
            if "redirect" in report:
                previous = report["redirect"]
                section = escape(previous["section"], quote=True)
                target = f'../{report["id"]}/#{section}'
                label = COPY[locale]["research"]["moved"]
                link = f'<a class="text-link" href="{target}">{escape(fields["title"])}</a>'
                body = page_intro(label, "", extra=link)
                write_page(locale, f'research/{previous["from"]}/', fields["title"], label, body, redirect=target)

"""Build the English and Simplified Chinese pages."""

import json
import re
from datetime import date
from hashlib import sha256
from html import escape
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
WORDMARK = (ROOT / "assets" / "brand.svg").read_text(encoding="utf-8").strip()
REPORT_CONTENT = ROOT / "content" / "research"
LEGAL_CONTENT = ROOT / "content" / "legal"
SITE_URL = "https://alphawink.com"
CONTACT = "hi@alphawink.com"
GITHUB = "https://github.com/vimday"
ROUTES = ("", "products/", "about/")
NAV_ROUTES = ("", "research/", "products/", "about/")
ENGINEERING_ROUTE = "engineering/"
LEGAL_ROUTES = ("privacy", "terms")
LEGAL_UPDATED = "2026-11-27"
PROJECTS = (
    ("aleph", "aleph-tx", "AlephTX", "https://github.com/AlephTX/aleph-tx",
     "raw/refs/heads/main/docs/QUICKSTART.md", "commit/5fe4251ce09341c6a6148571ab5b8606065db928", "tree/main/docs"),
    ("oasis", "oasis-agent", "Oasis Agent", "https://github.com/vimday/oasis-agent",
     "#quickstart", "commit/13acce072dfdfeb98e0cb2b0ad5af55308df997d", "tree/main/docs"),
)
ASSETS = {
    path: f"{path}?v={sha256((ROOT / path).read_bytes()).hexdigest()[:10]}"
    for path in (
        "assets/site.css",
        "assets/brand.js",
        "feed.js",
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
        "engineering_link": "Engineering portfolio",
        "footer": {
            "summary": "Research and software for on-chain markets.",
            "contact": "Contact",
            "address_label": "Hong Kong address",
            "address": "Hong Kong Industrial Building, 444-452 Des Voeux Road West, Sai Wan, Hong Kong",
            "copyright": "© 2026 AlphaWink. All rights reserved.",
            "links": "Site information",
        },
        "legal": {
            "updated": "Last updated",
            "privacy": ("Privacy Policy", "How AlphaWink handles information from site visits and email inquiries."),
            "terms": ("Terms of Service", "The terms for using AlphaWink’s website, research and project materials."),
        },
        "research": {
            "archive": "Research archive",
            "archive_intro": "Investigations into trading, market structure and risk.",
            "back": "All research",
            "read": "Read the report",
            "updated": "Updated",
            "contents": "In this report",
            "moved": "This report is now part of the full investigation.",
        },
        "alpha": {
            "label": "Web3 infrastructure · Early stage",
            "title": "Infrastructure for <span>on-chain markets</span>",
            "intro": "AlphaWink builds Web3 data infrastructure for quantitative research. Our tools capture activity from decentralized markets, retain the evidence and replay it to study liquidity and execution.",
            "browse": "Explore products",
            "contact": "Contact us",
            "featured": "Selected research",
            "method": "From data to evidence",
            "steps": (
                ("Capture market events", "Stream order books and trades from decentralized markets.", "WebSocket feeds"),
                ("Preserve the evidence", "Archive timestamped events, chain state and transaction receipts.", "Block hash · SHA-256"),
                ("Replay and simulate", "Reconstruct liquidity and test execution assumptions from retained inputs.", "Arrival-ordered tapes"),
            ),
            "feed": "Research notes",
            "filters": {"all": "All", "markets": "Market mechanics", "data": "Robotics data", "tools": "Research methods"},
            "empty": "No notes in this category yet.",
            "source": "Original source",
            "risk": "What to watch",
        },
        "products": {
            "title": "Systems for <span>on-chain research</span>",
            "intro": "AlephTX records and replays how perpetual markets trade. Oasis Agent reconstructs on-chain decisions and checks risk independently before execution.",
            "source": "View on GitHub",
            "start": "Quickstart",
            "changes": "Recent work",
            "commit": "View change",
            "docs": "Technical documentation",
            "roadmap": "Infrastructure roadmap",
            "directions": (
                ("Market data infrastructure", "We plan to use cloud object storage for reproducible event archives and compute workers for parallel replay and simulation."),
                ("Multimodal data R&D", "We’re exploring versioned data pipelines for AI that retain source provenance and validation results. GPU batch processing is a future research direction."),
            ),
            "access_title": "Work with AlphaWink",
            "access_intro": "Developing research workflows for on-chain markets? Tell us which data sources or replay tools you need.",
            "access": "Request early access",
            "aleph": {
                "topic": "Perpetual futures",
                "summary": "Multi-venue order books, causal replay and supervised execution in Rust and Go.",
                "detail": "AlephTX links three workflows. Its Go feeder and Rust strategy engine share a versioned market-data interface. A separate capture pipeline retains the data for replay, so research can evaluate a decision using the information available at the time.",
                "status": "MIT licensed",
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
            "title": "About AlphaWink",
            "intro": "AlphaWink is an early-stage technology and infrastructure R&D project. We develop data pipelines, low-latency analysis software and reproducible research tools for decentralized markets.",
            "founder": "Founder · Neo",
            "founder_intro": "My engineering work spans embodied AI data platforms and AI infrastructure, including workflows that turn multimodal robot data into datasets teams can validate and reuse.",
            "scope": "AlphaWink builds research software and publishes technical analysis. Visitors use the tools in their own environments. AlphaWink does not operate an exchange, hold customer assets or manage funds on behalf of others.",
            "contact": "Contact AlphaWink",
            "github": "GitHub profile",
            "work_areas": (
                ("Data platforms", "I build pipelines for processing, annotating, validating and versioning multimodal robot datasets."),
                ("AI infrastructure", "I develop distributed services that execute data workflows and deliver datasets for downstream AI workloads."),
                ("Workflow graph engine", "I built a graph engine from scratch that represents robot data processing as steps with explicit dependencies."),
                ("Advertising platform", "I worked on Go backend services for an advertising platform."),
            ),
            "tools": "Daily tools",
            "stack": (
                ("Coding agents", "Codex · Claude Code · MCP"),
                ("Terminal", "Herdr · Neovim · Linux · Git"),
                ("Systems", "Go · Rust · Python · Kubernetes · Docker"),
            ),
        },
        "engineering": {
            "name": "Neo · Engineering portfolio",
            "label": "Neo",
            "title": "Data platforms and <span>AI infrastructure</span>",
            "intro": "I build systems that turn raw data into artifacts teams can validate, replay and reuse. My work spans multimodal robotics data, workflow execution and low-latency research infrastructure.",
            "contact": "Get in touch",
            "work": "Engineering experience",
            "projects": "Public system designs",
            "jump": "Explore the case studies",
            "notes": "Engineering notes",
            "cases": (
                {
                    "id": "aleph-tx",
                    "name": "AlephTX",
                    "title": "Replay what the strategy could know",
                    "summary": "An analysis query wants a convenient view of market events. A simulation needs the exact order and timing in which inputs became available, including gaps. AlephTX keeps distinct representations for those two jobs.",
                    "detail": "The live path connects a Go WebSocket feeder to Rust over versioned shared memory. A separate capture path seals raw events with SHA-256 and produces Parquet partitions for queries and arrival-ordered replay tapes for simulation.",
                    "steps": ("Go WebSocket feeder", "Versioned shared memory", "Rust strategy engine"),
                    "flow": "Live data path",
                    "links": (
                        ("IPC protocol", "https://github.com/AlephTX/aleph-tx/raw/refs/heads/main/docs/DUAL_TRACK_IPC.md"),
                        ("Data and replay design", "https://github.com/AlephTX/aleph-tx/raw/refs/heads/main/docs/QUANT_DATA_LAKEHOUSE.md"),
                    ),
                },
                {
                    "id": "oasis-agent",
                    "name": "Oasis Agent",
                    "title": "Make replay safe to retry",
                    "summary": "A worker can die after claiming a job. A chain reorganization can invalidate its inputs. The replay scheduler needs recovery from both while keeping stale results out of the evidence record.",
                    "detail": "Oasis Agent commits replay jobs and coverage state together in SQLite. Workers retry under fenced leases. Completion is idempotent, and chain reorganizations invalidate affected work. Retained provider payloads tie each replay to its original inputs.",
                    "steps": ("Block-pinned inputs", "SQLite replay queue", "Evidence report"),
                    "flow": "Replay data path",
                    "links": (
                        ("Queue and recovery design", "https://github.com/vimday/oasis-agent/raw/refs/heads/main/docs/verification/CYCLE_OUTBOX_20261114.md"),
                        ("Feature pipeline", "https://github.com/vimday/oasis-agent/raw/refs/heads/main/docs/architecture/LP_MARKET_FEATURE_PIPELINE.md"),
                    ),
                },
            ),
        },
    },
    "zh": {
        "nav": ("首页", "研究", "产品", "关于"),
        "skip": "跳到正文",
        "nav_label": "网站导航",
        "engineering_link": "工程作品集",
        "footer": {
            "summary": "面向链上市场的研究与软件。",
            "contact": "联系邮箱",
            "address_label": "香港地址",
            "address": "香港西环德辅道西444-452号香港工业大厦",
            "copyright": "© 2026 AlphaWink. 保留所有权利。",
            "links": "站点信息",
        },
        "legal": {
            "updated": "最后更新",
            "privacy": ("隐私政策", "AlphaWink 如何处理网站访问和邮件联系涉及的信息。"),
            "terms": ("服务条款", "适用于 AlphaWink 网站、研究与项目资料的使用条款。"),
        },
        "research": {
            "archive": "研究归档",
            "archive_intro": "关于交易、市场结构和风险的深度研究。",
            "back": "全部研究",
            "read": "阅读全文",
            "updated": "更新于",
            "contents": "本文目录",
            "moved": "这篇报告已并入完整研究。",
        },
        "alpha": {
            "label": "Web3 基础设施 · 早期研发",
            "title": "为链上市场<span>构建数据基础设施</span>",
            "intro": "AlphaWink 为 Web3 量化研究开发数据基础设施。我们的工具采集去中心化市场数据，保留原始证据，再通过回放研究流动性与执行。",
            "browse": "查看产品",
            "contact": "联系我们",
            "featured": "研究选读",
            "method": "从数据到证据",
            "steps": (
                ("实时采集", "持续采集去中心化市场的订单簿与公开成交。", "WebSocket 行情"),
                ("保留证据", "归档带时间戳的事件、链上状态和交易回执。", "区块哈希 · SHA-256"),
                ("回放与模拟", "基于留存数据还原流动性，检验执行假设。", "按到达顺序记录"),
            ),
            "feed": "研究笔记",
            "filters": {"all": "全部", "markets": "市场机制", "data": "机器人数据", "tools": "研究方法"},
            "empty": "这个分类还没有笔记。",
            "source": "原始来源",
            "risk": "需要留意",
        },
        "products": {
            "title": "为链上研究<span>构建的系统</span>",
            "intro": "AlephTX 记录并回放永续合约市场。Oasis Agent 用原始证据复盘链上决策，在执行前独立校验风险。",
            "source": "GitHub 源码",
            "start": "快速开始",
            "changes": "近期更新",
            "commit": "查看提交",
            "docs": "技术文档",
            "roadmap": "基础设施路线图",
            "directions": (
                ("市场数据基础设施", "计划用云对象存储保存可复现的事件归档，并以计算集群并行运行回放和模拟。"),
                ("多模态数据研发", "探索面向 AI 的数据流水线，保留数据来源、版本和校验结果。GPU 批处理是后续的研发方向。"),
            ),
            "access_title": "与 AlphaWink 联系",
            "access_intro": "如果你在搭建链上市场的研究流程，欢迎告诉我们你需要哪些数据源或回放能力。",
            "access": "申请提前体验",
            "aleph": {
                "topic": "永续合约",
                "summary": "跨平台订单簿、因果回放与受监督执行，核心由 Rust 和 Go 实现。",
                "detail": "AlephTX 将采集、研究与执行连起来。Go 行情进程和 Rust 策略引擎通过版本化的共享内存接口交换数据，独立采集链路保存回放材料，让研究能按决策当时可见的信息检验策略。",
                "status": "MIT 许可",
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
            "title": "关于 AlphaWink",
            "intro": "AlphaWink 是一个处于早期阶段的技术与基础设施研发项目。我们面向去中心化市场开发数据管线、低延迟分析软件和可复现的研究工具。",
            "founder": "创始人 · Neo",
            "founder_intro": "我的工程工作涵盖具身智能数据平台与 AI 基础设施，包括将多模态机器人数据处理成可校验、可复用的数据集。",
            "scope": "AlphaWink 开发研究软件并发布技术分析，使用者在自己的环境中运行工具。AlphaWink 不运营交易所，不托管客户资产，也不提供代客资金管理。",
            "contact": "联系 AlphaWink",
            "github": "GitHub 主页",
            "work_areas": (
                ("数据平台", "构建多模态机器人数据流水线，覆盖处理、标注、质量校验和数据集版本管理。"),
                ("AI 基础设施", "建设分布式服务，支撑数据流程执行和面向下游 AI 工作负载的数据集交付。"),
                ("图流程引擎", "从零开发面向机器人数据处理的图流程引擎，用节点和显式依赖表达处理步骤。"),
                ("广告平台", "参与广告平台的 Go 后端服务开发。"),
            ),
            "tools": "日常工具",
            "stack": (
                ("编程 Agent", "Codex · Claude Code · MCP"),
                ("终端环境", "Herdr · Neovim · Linux · Git"),
                ("系统开发", "Go · Rust · Python · Kubernetes · Docker"),
            ),
        },
        "engineering": {
            "name": "Neo · 工程作品集",
            "label": "Neo",
            "title": "数据平台与 <span>AI 基础设施</span>",
            "intro": "我做数据平台和基础设施，把原始数据变成可校验、可回放、可复用的产物。工作涉及多模态机器人数据、流程执行和低延迟研究基础设施。",
            "contact": "联系我",
            "work": "工程经历",
            "projects": "公开系统设计",
            "jump": "查看项目案例",
            "notes": "工程笔记",
            "cases": (
                {
                    "id": "aleph-tx",
                    "name": "AlephTX",
                    "title": "只回放策略当时能看到的数据",
                    "summary": "分析查询需要易用的数据视图，模拟则要还原数据对策略可见的时点和顺序，还得保留采集缺口。AlephTX 为两种场景保留各自的数据表示。",
                    "detail": "实时链路中，Go 行情进程通过版本化共享内存向 Rust 策略引擎供数。独立采集链路用 SHA-256 校验原始归档，分别生成供查询的 Parquet 分区，以及按到达顺序生成的模拟回放文件。",
                    "steps": ("Go WebSocket 行情进程", "版本化共享内存", "Rust 策略引擎"),
                    "flow": "实时数据链路",
                    "links": (
                        ("进程间通信协议", "https://github.com/AlephTX/aleph-tx/raw/refs/heads/main/docs/DUAL_TRACK_IPC.md"),
                        ("数据与回放设计", "https://github.com/AlephTX/aleph-tx/raw/refs/heads/main/docs/QUANT_DATA_LAKEHOUSE.md"),
                    ),
                },
                {
                    "id": "oasis-agent",
                    "name": "Oasis Agent",
                    "title": "让回放在失败后安全重试",
                    "summary": "工作进程可能在领取任务后退出，链重组也可能让输入失效。回放调度既要能恢复任务，也要防止过期结果被写入证据记录。",
                    "detail": "Oasis Agent 在同一个 SQLite 事务中提交回放任务和覆盖状态。工作进程通过带校验的租约重试，重复完成操作保持幂等，遇到链重组则使受影响的任务失效。每次回放都能追溯到留存的原始数据响应。",
                    "steps": ("固定区块的输入", "SQLite 回放队列", "证据报告"),
                    "flow": "回放数据链路",
                    "links": (
                        ("队列与恢复设计", "https://github.com/vimday/oasis-agent/raw/refs/heads/main/docs/verification/CYCLE_OUTBOX_20261114.md"),
                        ("特征数据管线", "https://github.com/vimday/oasis-agent/raw/refs/heads/main/docs/architecture/LP_MARKET_FEATURE_PIPELINE.md"),
                    ),
                },
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
    if sum(report.get("featured") is True for report in reports) > 1:
        raise ValueError("Only one report can be featured on the homepage")
    return sorted(reports, key=lambda report: report["date"], reverse=True)


def report_path(report):
    return f'research/{report["id"]}/'


def report_meta(report, locale):
    topic = escape(report[locale]["topic"])
    day = report["date"]
    return f'<div class="report-meta"><span>{topic}</span><time datetime="{day}">{day}</time></div>'


def home(locale, root, here, notes, reports):
    locale_copy = COPY[locale]
    copy = locale_copy["alpha"]
    read = locale_copy["research"]["read"]
    lead = next((report for report in reports if report.get("featured") is True), None)
    feature = ""
    if lead:
        fields = lead[locale]
        feature = f"""
    <section class="section home-feature" id="reports" aria-labelledby="reports-title">
      <h2 class="kicker" id="reports-title">{copy["featured"]}</h2>
      <div class="home-feature-copy">
        {report_meta(lead, locale)}
        <h3><a href="{here}{report_path(lead)}">{escape(fields["title"])}</a></h3>
        <p>{escape(fields["summary"])}</p>
        <a class="text-link" href="{here}{report_path(lead)}">{read} <span aria-hidden="true">→</span></a>
      </div>
    </section>"""
    steps = "\n".join(
        f'          <li><h3>{title}</h3><p>{detail}</p><span class="flow-data">{data}</span></li>'
        for title, detail, data in copy["steps"]
    )
    note_ids = " ".join(note["id"] for note in notes)
    return f"""
    <section class="home-hero" aria-labelledby="title">
      <div class="home-intro">
        <p class="kicker">{copy["label"]}</p>
        <h1 id="title">{copy["title"]}</h1>
        <div class="home-deck">
          <p>{copy["intro"]}</p>
          <div class="home-actions">
            <a class="hero-link" href="{here}products/">{copy["browse"]} <span aria-hidden="true">→</span></a>
            <a class="text-link" href="mailto:{CONTACT}">{copy["contact"]} <span aria-hidden="true">↗</span></a>
          </div>
        </div>
      </div>
      <section class="system-flow" aria-labelledby="method-title">
        <h2 id="method-title">{copy["method"]}</h2>
        <ol role="list">
{steps}
        </ol>
        <a class="text-link flow-portfolio" href="{here}{ENGINEERING_ROUTE}">{locale_copy["engineering_link"]} <span aria-hidden="true">→</span></a>
      </section>
    </section>{feature}
    <script src="{root}{ASSETS["feed.js"]}" data-home-notes="{escape(note_ids, quote=True)}" defer></script>"""


def research_archive(reports, notes, locale):
    copy = COPY[locale]["research"]
    entries = "".join(f"""
      <article class="report-entry">
        {report_meta(report, locale)}
        <h2><a href="../{report_path(report)}">{escape(report[locale]["title"])}</a></h2>
        <p>{escape(report[locale]["summary"])}</p>
      </article>""" for report in reports)
    notes_copy = COPY[locale]["alpha"]
    notes_link = f'<a class="text-link" href="#feed">{notes_copy["feed"]} <span aria-hidden="true">↓</span></a>' if notes else ""
    intro = page_intro(copy["archive"], copy["archive_intro"], extra=notes_link)
    root = "../../" if locale == "zh" else "../"
    return intro + f'<div class="research-archive">{entries}</div>' + research_notes(locale, root, notes, notes_copy)


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


def research_notes(locale, root, notes, copy):
    if not notes:
        return ""
    categories = {entry["category"] for entry in notes}
    filters = "\n".join(
        f'        <button type="button" data-filter="{key}" aria-pressed="{str(key == "all").lower()}">{label}</button>'
        for key, label in copy["filters"].items()
        if key == "all" or key in categories
    )
    return f"""
    <section class="section" id="feed" aria-labelledby="feed-title">
      <div class="section-header">
        <h2 id="feed-title">{copy["feed"]}</h2>
        <div id="filters" class="filters" role="group" aria-label="{copy["feed"]}" hidden>
{filters}
        </div>
      </div>
      <div id="notes" class="note-index">{render_notes(notes, locale, copy)}
      </div>
      <p id="empty" class="empty" hidden>{copy["empty"]}</p>
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
              <a class="text-link" href="{repo}/{docs}">{copy["docs"]} <span aria-hidden="true">↗</span></a>
            </div>
          </div>
        </div>
      </article>""")
    names = "".join(f'<a class="text-link" href="#{slug}">{name} <span aria-hidden="true">↓</span></a>'
                    for _, slug, name, *_ in PROJECTS)
    directions = "\n".join(
        f"      <div><h3>{title}</h3><p>{detail}</p></div>" for title, detail in copy["directions"]
    )
    return page_intro(copy["title"], copy["intro"], masthead=True) + f"""
    <div class="product-jump">{names}</div>
    <div class="product-list" id="research-walkthrough">{"".join(cards)}
    </div>
    <section class="section editorial-split" aria-labelledby="roadmap-title">
      <h2 id="roadmap-title">{copy["roadmap"]}</h2>
      <div class="roadmap-entries">
{directions}
      </div>
    </section>
    <section class="section editorial-split access-section" aria-labelledby="access-title">
      <h2 id="access-title">{copy["access_title"]}</h2>
      <div>
        <p>{copy["access_intro"]}</p>
        <a class="hero-link" href="mailto:{CONTACT}">{copy["access"]} <span aria-hidden="true">↗</span></a>
      </div>
    </section>"""


def about(here, copy):
    about_copy = copy["about"]
    contact = f'<a class="text-link" href="mailto:{CONTACT}">{about_copy["contact"]} <span aria-hidden="true">↗</span></a>'
    return page_intro(about_copy["title"], about_copy["intro"], extra=contact) + f"""
    <section class="section editorial-split founder-section" aria-labelledby="founder-title">
      <h2 id="founder-title">{about_copy["founder"]}</h2>
      <div>
        <p>{about_copy["founder_intro"]}</p>
        <div class="engineering-links">
          <a class="text-link" href="{here}{ENGINEERING_ROUTE}">{copy["engineering_link"]} <span aria-hidden="true">→</span></a>
          <a class="text-link" href="{GITHUB}">{about_copy["github"]} <span aria-hidden="true">↗</span></a>
        </div>
      </div>
    </section>
    <p class="site-scope">{about_copy["scope"]}</p>"""


def engineering_case(case, projects_copy):
    slug = case["id"]
    repository = next(repo for _, project, _, repo, *_ in PROJECTS if project == slug)
    stages = "".join(f"<li>{stage}</li>" for stage in case["steps"])
    links = "\n".join(
        f'        <a class="text-link" href="{url}">{label} <span aria-hidden="true">↗</span></a>'
        for label, url in (*case["links"], (projects_copy["source"], repository))
    )
    return f"""
      <article class="engineering-case" id="{slug}" aria-labelledby="{slug}-title">
        <div class="case-copy">
          <p class="kicker">{case["name"]}</p>
          <h3 id="{slug}-title">{case["title"]}</h3>
          <p>{case["summary"]}</p>
          <p>{case["detail"]}</p>
        </div>
        <figure class="case-flow">
          <figcaption>{case["flow"]}</figcaption>
          <ol role="list">{stages}</ol>
        </figure>
        <div class="engineering-links case-links">
{links}
        </div>
      </article>"""


def write_engineering_page(locale, notes):
    locale_copy = COPY[locale]
    copy = locale_copy["engineering"]
    about_copy = locale_copy["about"]
    areas = "\n".join(
        f"      <article><h3>{title}</h3><p>{description}</p></article>"
        for title, description in about_copy["work_areas"]
    )
    cases = "".join(engineering_case(case, locale_copy["products"]) for case in copy["cases"])
    stack = "".join(f"<div><dt>{area}</dt><dd>{tools}</dd></div>" for area, tools in about_copy["stack"])
    archive = ""
    if notes:
        archive = f"""
    <section class="section archive-section" aria-labelledby="archive-title">
      <h2 id="archive-title">{copy["notes"]}</h2>
      <div class="archive-grid">{render_notes(notes, locale, locale_copy["alpha"])}
      </div>
    </section>"""
    body = f"""
    <section class="page-intro engineering-hero" aria-labelledby="title">
      <div>
        <p class="kicker">{copy["label"]}</p>
        <h1 id="title">{copy["title"]}</h1>
      </div>
      <div>
        <p class="intro">{copy["intro"]}</p>
        <div class="engineering-links">
          <a class="text-link" href="mailto:{CONTACT}">{copy["contact"]} <span aria-hidden="true">↗</span></a>
          <a class="text-link" href="{GITHUB}">{about_copy["github"]} <span aria-hidden="true">↗</span></a>
        </div>
      </div>
    </section>
    <section class="section work-section" aria-labelledby="work-title">
      <div class="section-header">
        <h2 id="work-title">{copy["work"]}</h2>
        <a class="text-link" href="#case-studies">{copy["jump"]} <span aria-hidden="true">↓</span></a>
      </div>
      <div class="grid work-grid">
{areas}
      </div>
    </section>
    <section class="section case-section" aria-labelledby="case-studies">
      <h2 id="case-studies">{copy["projects"]}</h2>{cases}
    </section>
    <section class="section tool-section" aria-labelledby="tools-title">
      <h2 id="tools-title">{about_copy["tools"]}</h2>
      <dl class="tool-grid">{stack}</dl>
    </section>{archive}"""
    write_page(locale, ENGINEERING_ROUTE, copy["name"], copy["intro"], body)


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
        body = home(locale, root, here, market_notes, reports)
    elif page == 1:
        body = products(section)
    else:
        body = about(here, copy)
    write_page(locale, path, name, description, body)


def write_legal_pages(locale):
    copy = COPY[locale]["legal"]
    updated = f'<p class="legal-date">{copy["updated"]} <time datetime="{LEGAL_UPDATED}">{LEGAL_UPDATED}</time></p>'
    for page in LEGAL_ROUTES:
        title, description = copy[page]
        sections = (LEGAL_CONTENT / f"{page}.{locale}.html").read_text(encoding="utf-8").strip()
        body = page_intro(title, description, extra=updated) + f"""
    <article class="legal-prose" aria-labelledby="title">
      {sections}
    </article>"""
        write_page(locale, f"{page}/", title, description, body)


def write_page(locale, path, name, description, body, *, redirect=None):
    copy = COPY[locale]
    lang = "zh-Hans" if locale == "zh" else "en"
    route = ("zh/" if locale == "zh" else "") + path
    root = "../" * route.count("/") or "./"
    here = root + ("zh/" if locale == "zh" else "")
    other_lang, other_label = ("en", "English") if locale == "zh" else ("zh-Hans", "中文")
    other = root + ("zh/" if locale == "en" else "") + path
    current = {path: ' aria-current="page"'}
    if path.startswith("research/") and path != "research/":
        current["research/"] = ' aria-current="location"'
    if path == ENGINEERING_ROUTE:
        current["about/"] = ' aria-current="location"'
    nav = [
        f'      <a href="{here}{nav_path}"{current.get(nav_path, "")}>{label}</a>'
        for nav_path, label in zip(NAV_ROUTES, copy["nav"], strict=True)
    ]
    nav_start = "\n".join(nav[:2])
    nav_end = "\n".join(nav[2:])
    footer = copy["footer"]
    legal_links = "\n".join(
        f'        <a href="{here}{page}/"{current.get(page + "/", "")}>{copy["legal"][page][0]}</a>'
        for page in LEGAL_ROUTES
    )
    canonical = f"{SITE_URL}/{route}"
    redirect_head = ""
    if redirect:
        target = escape(redirect, quote=True)
        redirect_head = f'\n  <meta http-equiv="refresh" content="0; url={target}">'
        canonical = urljoin(canonical, redirect.split("#", 1)[0])
    html = f"""<!-- Copyright 2025 vimday; SPDX-License-Identifier: Apache-2.0 -->
<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(description, quote=True)}">
  <meta name="theme-color" content="#fcfcfa">
  <title>{escape(name)} / AlphaWink</title>
  <link rel="icon" href="{root}{ASSETS["favicon.ico"]}" sizes="16x16 32x32 48x48" type="image/x-icon">
  <link rel="icon" href="{root}{ASSETS["favicon-32x32.png"]}" sizes="32x32" type="image/png">
  <link rel="icon" href="{root}{ASSETS["favicon-96x96.png"]}" sizes="96x96" type="image/png">
  <link rel="apple-touch-icon" href="{root}{ASSETS["apple-touch-icon.png"]}" sizes="180x180">
  <link rel="stylesheet" href="{root}{ASSETS["assets/site.css"]}">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="{other_lang}" href="{other}">{redirect_head}
</head>
<body>
  <a class="skip" href="#main">{copy["skip"]}</a>
  <header class="site-header">
    <div class="bar wrap">
      <a class="brand" href="{here}" aria-label="AlphaWink">
        {WORDMARK}
      </a>
      <nav aria-label="{copy["nav_label"]}">
        <div class="nav-group">
{nav_start}
        </div>
        <div class="nav-group">
{nav_end}
        </div>
      </nav>
    </div>
  </header>
  <main class="wrap" id="main">{body}
  </main>
  <footer class="wrap footer">
    <div class="footer-main">
      <div class="footer-identity">
        <a href="{here}">AlphaWink</a>
        <p>{footer["summary"]}</p>
      </div>
      <div>
        <p class="footer-label">{footer["contact"]}</p>
        <a href="mailto:{CONTACT}">{CONTACT}</a>
      </div>
      <div>
        <p class="footer-label">{footer["address_label"]}</p>
        <address>{footer["address"]}</address>
      </div>
    </div>
    <div class="footer-base">
      <p>{footer["copyright"]}</p>
      <nav class="footer-links" aria-label="{footer["links"]}">
        <a href="{here}{ENGINEERING_ROUTE}"{current.get(ENGINEERING_ROUTE, "")}>{copy["engineering_link"]}</a>
{legal_links}
        <a href="{other}" lang="{other_lang}" hreflang="{other_lang}">{other_label}</a>
      </nav>
    </div>
  </footer>
  <script src="{root}{ASSETS["assets/brand.js"]}" defer></script>
</body>
</html>
"""
    destination = ROOT / route
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    notes = read_notes()
    reports = read_reports()
    market_notes = [note for note in notes if note["category"] != "data"]
    engineering_notes = [note for note in notes if note["category"] == "data"]
    for locale in COPY:
        for page in range(len(ROUTES)):
            render(locale, page, notes, reports)
        write_engineering_page(locale, engineering_notes)
        write_legal_pages(locale)
        archive = COPY[locale]["research"]
        write_page(locale, "research/", archive["archive"], archive["archive_intro"], research_archive(reports, market_notes, locale))
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

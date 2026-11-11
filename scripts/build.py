"""Regenerate the bilingual static pages with Python 3."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COPY = {
    "en": {
        "nav": ("Alpha", "Products", "About me"),
        "skip": "Skip to content",
        "contact": "Email",
        "alpha": (
            "OPPORTUNITY NOTES",
            "Find the signal.",
            "Research notes on markets, data, and tools. Each note explains what changed, where to verify it, and what could invalidate it.",
            "Read the feed",
            "What we look for",
            ("What changed?", "Where's the evidence?", "What could break the thesis?"),
            "Latest notes",
            "No notes published yet. The first entries will appear here.",
            "Have a lead? Send the source and what caught your eye.",
            "Send a lead",
        ),
        "products": (
            "Two projects in development.",
            "AlephTX and Oasis Agent are projects we’re building. This page introduces what each is for and will carry public access links when they’re ready.",
            (
                ("AlephTX", "PERPETUAL FUTURES", "Execution and relative-value research for perpetual futures. Replay recorded market data to test how a strategy behaves after fees, funding, and slippage."),
                ("Oasis Agent", "RESEARCH & RISK", "A market research agent that keeps the evidence behind each decision. Replay the reasoning and evaluate risk limits before execution."),
            ),
            "In development",
        ),
        "about": (
            "Hi, I'm Neo.",
            "I build data platforms for embodied AI and work on AI infrastructure. Outside work, I build terminal tools and experiment with agents and systems I can inspect and replay.",
            "On my workbench",
            "My GitHub profile",
        ),
    },
    "zh": {
        "nav": ("Alpha 机会", "产品", "关于我"),
        "skip": "跳到正文",
        "contact": "邮件",
        "alpha": (
            "机会笔记",
            "寻找值得验证的机会。",
            "关注市场、数据和工具。每条笔记都说明发生了什么、去哪里核实，以及什么情况会让判断失效。",
            "看最新笔记",
            "我们关注什么",
            ("发生了什么变化？", "证据在哪里？", "什么会推翻这个判断？"),
            "最新笔记",
            "还没有发布笔记。第一批内容会在这里更新。",
            "发现了值得关注的线索？欢迎发来源和你看到的变化。",
            "分享线索",
        ),
        "products": (
            "正在开发的两个项目。",
            "这里介绍 AlephTX 和 Oasis Agent 的用途。开放使用后，我们会在这里更新入口。",
            (
                ("AlephTX", "永续合约", "用于永续合约执行和相对价值研究。回放记录下来的市场数据，观察策略在计入手续费、资金费率和滑点后的表现。"),
                ("Oasis Agent", "研究与风控", "一个市场研究 Agent，保留每个判断所依据的证据，支持回放研究过程，并在执行前检查风险约束。"),
            ),
            "开发中",
        ),
        "about": (
            "你好，我是 Neo。",
            "我的主业是具身智能数据平台和 AI 基础设施开发。工作之外，我喜欢写终端工具，也会研究 Agent 和能回放、能检查的系统。",
            "我的工作台",
            "我的 GitHub 主页",
        ),
    },
}
ROUTES = ("", "products/", "about/")


def alpha(root, copy):
    kicker, title, intro, browse, format_title, prompts, latest, empty, share, send = copy["alpha"]
    items = "".join(f"<li>{prompt}</li>" for prompt in prompts)
    return f"""
    <section class="hero" aria-labelledby="title">
      <div>
        <p class="kicker"><span aria-hidden="true">●</span> {kicker}</p>
        <h1 id="title">{title[:-1]}<span>{title[-1]}</span></h1>
        <p class="intro">{intro}</p>
        <div class="links"><a class="primary" href="#feed">{browse} <span aria-hidden="true">↓</span></a></div>
      </div>
      <aside class="terminal">
        <div class="terminal-bar"><span class="lights" aria-hidden="true"><i></i><i></i><i></i></span> alphawink / field notes</div>
        <div class="terminal-body">
          <p class="prompt"><span>$</span> cat ~/checklist.txt</p>
          <h2 class="format-title">{format_title}</h2>
          <ol class="checklist">{items}</ol>
        </div>
      </aside>
    </section>
    <section class="projects" id="feed" aria-labelledby="feed-title">
      <p class="kicker"><span aria-hidden="true">//</span> ALPHA</p>
      <h2 id="feed-title">{latest}</h2>
      <div id="notes" data-feed="{root}opportunities.json" class="notes">
        <p class="empty">{empty}</p>
      </div>
      <p class="share">{share} <a href="mailto:ms0x7f@gmail.com?subject=AlphaWink%20lead">{send} <span aria-hidden="true">↗</span></a></p>
    </section>
    <script src="{root}feed.js" defer></script>"""


def products(copy):
    title, intro, entries, status = copy["products"]
    cards = "\n".join(
        f"""        <article class="project">
          <p class="tag">{area}</p>
          <h2>{name}</h2>
          <p>{description}</p>
          <span class="status">{status}</span>
        </article>"""
        for name, area, description in entries
    )
    return f"""
    <section class="page-intro" aria-labelledby="title">
      <p class="kicker"><span aria-hidden="true">//</span> ~/products</p>
      <h1 id="title">{title}</h1>
      <p class="intro">{intro}</p>
    </section>
    <div class="grid product-grid">
{cards}
    </div>"""


def about(copy):
    title, intro, setup, github = copy["about"]
    return f"""
    <section class="page-intro" aria-labelledby="title">
      <p class="kicker"><span aria-hidden="true">//</span> NEO / @VIMDAY</p>
      <h1 id="title">{title}</h1>
      <p class="intro">{intro}</p>
      <div class="links"><a class="primary" href="https://github.com/vimday">{github} <span aria-hidden="true">↗</span></a></div>
    </section>
    <section class="projects about-stack" aria-labelledby="stack-title">
      <h2 id="stack-title">{setup}</h2>
      <p>Linux · Neovim · Rust · Go · Python · MCP</p>
    </section>"""


def render(locale, page):
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
    description = (
        copy["alpha"][2], copy["products"][1], copy["about"][1]
    )[page]
    body = (lambda: alpha(root, copy), lambda: products(copy), lambda: about(copy))[page]()
    html = f"""<!-- Copyright 2025 vimday; SPDX-License-Identifier: Apache-2.0 -->
<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{description}">
  <meta name="theme-color" content="#0b110f">
  <title>AlphaWink — {name}</title>
  <link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{root}workbench.css">
  <link rel="alternate" hreflang="{other_lang}" href="{other}">
</head>
<body>
  <a class="skip" href="#main">{copy["skip"]}</a>
  <header class="bar wrap">
    <a class="brand" href="{here}"><span aria-hidden="true">&gt;_</span> alphawink</a>
    <nav aria-label="{'网站导航' if locale == 'zh' else 'Site navigation'}">
{nav}
      <a class="lang" href="{other}" lang="{other_lang}" hreflang="{other_lang}">{other_label}</a>
    </nav>
  </header>
  <main class="wrap" id="main">{body}
  </main>
  <footer class="wrap footer">
    <span><span aria-hidden="true">~/</span> AlphaWink</span>
    <a href="mailto:ms0x7f@gmail.com">{copy["contact"]} <span aria-hidden="true">↗</span></a>
  </footer>
</body>
</html>
"""
    target = ROOT / route / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    for locale in COPY:
        for page in range(len(ROUTES)):
            render(locale, page)

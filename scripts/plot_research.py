"""Render the research figures in English and Simplified Chinese."""

from argparse import ArgumentParser
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np


OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "research"
PAPER = "#eee8dd"
INK = "#24221e"
MUTED = "#5c554c"
RULE = "#cfc2b2"
ACCENT = "#8a422e"


def style_axes(axis):
    axis.set_facecolor(PAPER)
    axis.set_axisbelow(True)
    axis.tick_params(colors=MUTED, length=0, pad=9, labelsize=10)
    for spine in axis.spines.values():
        spine.set_visible(False)


def timeline(locale, font):
    # First row is the Ethereum transfer. The others are announcement timestamps.
    hours = [10 + 11 / 60 + 47 / 3600, 11 + 2 / 60 + 33 / 3600, 12 + 49 / 60 + 9 / 3600, 18 + 21 / 60 + 30 / 3600]
    stamps = ("10:11", "11:02", "12:49", "18:21")
    if locale == "zh":
        title = "从转出到恢复充提"
        labels = ("结算合约转出", "公告暂停提款与建池", "公告归因与 Guardian", "公告恢复充提")
    else:
        title = "From outflow to reopening"
        labels = ("Settlement outflow", "Pause announced", "Key leak and Guardian", "Transfers resumed")

    fig, axis = plt.subplots(figsize=(7, 3.65), facecolor=PAPER)
    fig.subplots_adjust(left=.36, right=.95, top=.72, bottom=.16)
    fig.text(.045, .89, title, color=INK, fontproperties=font, fontsize=17)
    fig.text(.045, .805, "2026-11-16  /  UTC", color=MUTED, family="monospace", fontsize=10)
    style_axes(axis)
    axis.set(xlim=(9.8, 19.55), ylim=(-.5, 3.5), yticks=[])
    start_hours = (10, 12, 14, 16, 18)
    axis.set_xticks(start_hours, [f"{hour}:00" for hour in start_hours])
    axis.grid(axis="x", color=RULE, linewidth=.65, alpha=.65)
    for row, (time, stamp, label) in enumerate(zip(hours, stamps, labels, strict=True)):
        y = 3 - row
        axis.axhline(y, color=RULE, linewidth=.7)
        axis.text(9.45, y, label, ha="right", va="center", color=INK, fontproperties=font, fontsize=11)
        axis.plot(time, y, "o", color=ACCENT, markerfacecolor=ACCENT if row == 0 else PAPER, markersize=6)
        axis.annotate(stamp, (time, y), xytext=(9, 1), textcoords="offset points", va="center", fontsize=10, color=ACCENT,
                      bbox={"facecolor": PAPER, "edgecolor": "none", "pad": 1.5})
    fig.savefig(OUTPUT / f"lighter-timeline-{locale}.png", dpi=200)
    plt.close(fig)


def withdrawal_budget(locale, font):
    minutes = np.linspace(0, 8, 161)
    requests = minutes
    release_ceiling = np.minimum(requests, 2 + .25 * minutes)
    if locale == "zh":
        title, units, duration = "提款额度如何压住突发流出", "累计金额（百万美元）", "经过时间（分钟）"
        demand, allowed = "累计请求", "放行上界"
    else:
        title, units, duration = "A ceiling on burst withdrawals", "Cumulative amount (USD millions)", "Elapsed minutes"
        demand, allowed = "Requested", "Release ceiling"

    fig, axis = plt.subplots(figsize=(7, 4.05), facecolor=PAPER)
    fig.subplots_adjust(left=.09, right=.94, top=.71, bottom=.185)
    fig.text(.045, .9, title, color=INK, fontproperties=font, fontsize=17)
    fig.text(.045, .815, units, color=MUTED, fontproperties=font, fontsize=11)
    style_axes(axis)
    axis.set(xlim=(0, 8.4), ylim=(0, 8.7), xticks=(0, 2, 4, 6, 8), yticks=(0, 2, 4, 6, 8))
    axis.grid(axis="y", color=RULE, linewidth=.65)
    axis.set_xlabel(duration, color=MUTED, fontproperties=font, fontsize=10, labelpad=7)
    axis.fill_between(minutes, release_ceiling, requests, color="#c28b75", alpha=.23)
    axis.plot(minutes, requests, linestyle="--", color=MUTED, linewidth=1.5)
    axis.plot(minutes, release_ceiling, color=ACCENT, linewidth=2)
    axis.plot(8, 8, "o", color=MUTED, markersize=4)
    axis.plot(8, 4, "o", color=ACCENT, markersize=4)
    axis.annotate(f"{demand}  8.0", (8, 8), xytext=(-11, 10), textcoords="offset points", ha="right",
                  color=MUTED, fontproperties=font, fontsize=11)
    axis.annotate(f"{allowed}  4.0", (8, 4), xytext=(-11, -17), textcoords="offset points", ha="right",
                  color=ACCENT, fontproperties=font, fontsize=11)
    fig.savefig(OUTPUT / f"withdrawal-budget-{locale}.png", dpi=200)
    plt.close(fig)


def incident_amounts(locale, font):
    if locale == "zh":
        title = "三起事件的金额证据"
        subtitle = "百万美元或美元稳定币面值 · 每行单独阅读"
        labels = ("Lighter · 结算合约流出", "Lighter · 平台披露返还", "Lighter · 外部账户估计",
                  "Arcus · 披露链上付款", "Arcus · 待付请求被拦截", "Aster · 当事人申报")
    else:
        title = "The amounts reported in three incidents"
        subtitle = "Millions of dollars or stablecoins at face value · read rows separately"
        labels = ("Lighter · on-chain outflow", "Lighter · return disclosed", "Lighter · external estimate",
                  "Arcus · payout disclosed", "Arcus · requests held", "Aster · user claim")

    values = (10.393056789298, 5, 15.5, 2.234391, 3, 4.5646755)
    labels_at_value = ("10.39", "~5.00", "~15.5", "2.23", "~3.00", "~4.56")
    markers = ("o", "o", "s", "o", "o", "D")
    fig, axis = plt.subplots(figsize=(7, 4.65), facecolor=PAPER)
    fig.subplots_adjust(left=.46, right=.955, top=.74, bottom=.13)
    fig.text(.045, .91, title, color=INK, fontproperties=font, fontsize=17)
    fig.text(.045, .825, subtitle, color=MUTED, fontproperties=font, fontsize=10.5)
    style_axes(axis)
    axis.set(xlim=(0, 18.8), ylim=(-.55, 5.55), yticks=[])
    axis.set_xticks((0, 5, 10, 15))
    axis.grid(axis="x", color=RULE, linewidth=.65)
    for row, (label, value, display, marker) in enumerate(zip(labels, values, labels_at_value, markers, strict=True)):
        y = 5 - row
        axis.axhline(y, color=RULE, linewidth=.6)
        axis.text(-.65, y, label, ha="right", va="center", color=INK, fontproperties=font, fontsize=12.5)
        axis.plot(value, y, marker=marker, color=ACCENT, markerfacecolor=ACCENT if row == 0 else PAPER, markersize=6)
        axis.annotate(display, (value, y), xytext=(8, 0), textcoords="offset points", va="center", color=ACCENT,
                      fontsize=12, bbox={"facecolor": PAPER, "edgecolor": "none", "pad": 1})
    fig.savefig(OUTPUT / f"incident-amounts-{locale}.png", dpi=200)
    plt.close(fig)


def custody_snapshots(locale, font):
    title = "六个历史资金观测值" if locale == "zh" else "Six historical snapshots of funds"
    subtitle = "美元计价 · 对数轴 · 日期和口径见表" if locale == "zh" else "USD values · log scale · dates and scopes in the table"
    venues = ("Hyperliquid", "Lighter", "Aster", "Variational", "GRVT", "Arcus")
    amounts = (6500, 1000, 500, 290, 63.5, 28)
    displays = ("~6.5B", "~1B", "~500M", "~290M", "~63.5M", "≥28M")
    fig, axis = plt.subplots(figsize=(7, 4.35), facecolor=PAPER)
    fig.subplots_adjust(left=.26, right=.955, top=.73, bottom=.145)
    fig.text(.045, .91, title, color=INK, fontproperties=font, fontsize=17)
    fig.text(.045, .82, subtitle, color=MUTED, fontproperties=font, fontsize=10)
    style_axes(axis)
    axis.set(xscale="log", xlim=(16, 17000), ylim=(-.55, 5.55), yticks=[])
    axis.set_xticks((20, 100, 1000, 10000), ("20M", "100M", "1B", "10B"))
    axis.minorticks_off()
    axis.grid(axis="x", color=RULE, linewidth=.65)
    for row, (venue, amount, display) in enumerate(zip(venues, amounts, displays, strict=True)):
        y = 5 - row
        axis.axhline(y, color=RULE, linewidth=.6)
        axis.text(14.5, y, venue, ha="right", va="center", color=INK, fontproperties=font, fontsize=13)
        axis.plot(amount, y, "o", color=ACCENT, markerfacecolor=PAPER, markersize=6)
        axis.annotate(display, (amount, y), xytext=(8, 0), textcoords="offset points", va="center", color=ACCENT,
                      fontsize=12, bbox={"facecolor": PAPER, "edgecolor": "none", "pad": 1})
    fig.savefig(OUTPUT / f"custody-snapshots-{locale}.png", dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--cjk-font", type=Path, required=True, help="A local font with Simplified Chinese glyphs")
    args = parser.parse_args()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for locale, font in (("en", FontProperties(family="DejaVu Sans")), ("zh", FontProperties(fname=args.cjk_font))):
        timeline(locale, font)
        withdrawal_budget(locale, font)
        incident_amounts(locale, font)
        custody_snapshots(locale, font)

"""Render the four research figures with Matplotlib."""

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


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--cjk-font", type=Path, required=True, help="A local font with Simplified Chinese glyphs")
    args = parser.parse_args()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for locale, font in (("en", FontProperties(family="DejaVu Sans")), ("zh", FontProperties(fname=args.cjk_font))):
        timeline(locale, font)
        withdrawal_budget(locale, font)

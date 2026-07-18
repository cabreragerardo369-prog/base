import os

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

from config import SYMBOL, TIMEFRAME, START_DATE, END_DATE

CSV_PATH = os.path.join("data", f"{SYMBOL}_{TIMEFRAME}_{START_DATE}_{END_DATE}.csv")
CHARTS_DIR = "charts"

COLOR_LINE = "#2a78d6"
COLOR_GRID = "#e1e0d9"
COLOR_AXIS = "#c3c2b7"
COLOR_TEXT_PRIMARY = "#0b0b0b"
COLOR_TEXT_MUTED = "#898781"
COLOR_SURFACE = "#fcfcfb"


def main():
    df = pd.read_csv(CSV_PATH, parse_dates=["timestamp"])

    fig, ax = plt.subplots(figsize=(12, 6), facecolor=COLOR_SURFACE)
    ax.set_facecolor(COLOR_SURFACE)

    ax.plot(df["timestamp"], df["close"], color=COLOR_LINE, linewidth=2)

    ax.set_title(f"{SYMBOL} — precio de cierre ({TIMEFRAME})", color=COLOR_TEXT_PRIMARY, fontsize=14, loc="left")
    ax.set_ylabel("Precio (USD)", color=COLOR_TEXT_MUTED)

    ax.grid(True, color=COLOR_GRID, linewidth=0.8)
    ax.set_axisbelow(True)

    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(COLOR_AXIS)

    ax.tick_params(colors=COLOR_TEXT_MUTED)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

    os.makedirs(CHARTS_DIR, exist_ok=True)
    output_path = os.path.join(CHARTS_DIR, f"{SYMBOL}_{TIMEFRAME}_close.png")
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"Guardado en {output_path}")


if __name__ == "__main__":
    main()

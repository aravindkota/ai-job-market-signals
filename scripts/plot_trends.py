#!/usr/bin/env python3
"""
Generate demo trend graphs (2023–2025) for two example skills
from data/trends_2023_2025.csv and save PNGs under assets/.

Outputs:
  - assets/trend_line.png        (monthly trend lines)
  - assets/indexed_trend.png     (indexed to 100 at first month)
  - assets/yoy_growth.png        (year-over-year % growth bars)

Requires: pandas, matplotlib, seaborn (optional styling)
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "trends_2023_2025.csv"
ASSETS = ROOT / "assets"


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["date"])  # columns: date, data_science, gen_ai
    df = df.sort_values("date").reset_index(drop=True)
    return df


def plot_trend_lines(df: pd.DataFrame, out: Path) -> None:
    plt.style.use("seaborn-v0_8") if "seaborn" in plt.style.available else None
    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=150)
    ax.plot(df["date"], df["data_science"], label="Data Science", linewidth=2)
    ax.plot(df["date"], df["gen_ai"], label="Generative AI", linewidth=2)
    ax.set_title("Monthly Trend (Demo Data)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Volume (Indexed Units)")
    ax.grid(True, alpha=0.2)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)


def plot_indexed(df: pd.DataFrame, out: Path) -> None:
    base = df.iloc[0]
    idx_ds = (df["data_science"] / base["data_science"]) * 100.0
    idx_ga = (df["gen_ai"] / base["gen_ai"]) * 100.0

    plt.style.use("seaborn-v0_8") if "seaborn" in plt.style.available else None
    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=150)
    ax.plot(df["date"], idx_ds, label="Data Science (Index=100)", linewidth=2)
    ax.plot(df["date"], idx_ga, label="Generative AI (Index=100)", linewidth=2)
    ax.set_title("Indexed Trend (Base = First Month)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Index (Base=100)")
    ax.grid(True, alpha=0.2)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)


def plot_yoy(df: pd.DataFrame, out: Path) -> None:
    # Compute YoY growth by comparing to value 12 months prior when available
    df = df.copy()
    df["ds_yoy"] = df["data_science"].pct_change(periods=12) * 100.0
    df["ga_yoy"] = df["gen_ai"].pct_change(periods=12) * 100.0
    yoy_df = df.dropna(subset=["ds_yoy", "ga_yoy"]).copy()

    if yoy_df.empty:
        return

    plt.style.use("seaborn-v0_8") if "seaborn" in plt.style.available else None
    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=150)
    width = 8
    ax.bar(yoy_df["date"].dt.to_pydatetime(), yoy_df["ds_yoy"], width=20, alpha=0.7, label="Data Science YoY %")
    ax.bar(yoy_df["date"].dt.to_pydatetime(), yoy_df["ga_yoy"], width=8, alpha=0.7, label="Generative AI YoY %")
    ax.set_title("Year-over-Year Growth (Demo Data)")
    ax.set_xlabel("Date")
    ax.set_ylabel("YoY %")
    ax.grid(True, axis="y", alpha=0.2)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate demo job-market trend graphs")
    parser.add_argument("--input", type=str, default=str(DATA), help="Path to CSV (date,data_science,gen_ai)")
    parser.add_argument("--outdir", type=str, default=str(ASSETS), help="Output directory for PNGs")
    args = parser.parse_args()

    csv_path = Path(args.input)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = load_data(csv_path)
    plot_trend_lines(df, outdir / "trend_line.png")
    plot_indexed(df, outdir / "indexed_trend.png")
    plot_yoy(df, outdir / "yoy_growth.png")

    print(f"Wrote: {outdir / 'trend_line.png'}")
    print(f"Wrote: {outdir / 'indexed_trend.png'}")
    print(f"Wrote: {outdir / 'yoy_growth.png'}")


if __name__ == "__main__":
    main()


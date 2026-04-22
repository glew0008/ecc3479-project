from __future__ import annotations

import re
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns

matplotlib.use("Agg")
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "clean" / "merged_2016_2021.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "eda"
FIGURES_DIR = OUTPUT_DIR / "figures"
TABLES_DIR = OUTPUT_DIR / "tables"
REPORT_PATH = OUTPUT_DIR / "eda_report.md"

EDUCATION_ORDER = [
    "Postgraduate Degree Level",
    "Graduate Diploma and Graduate Certificate Level",
    "Bachelor Degree Level",
    "Advanced Diploma and Diploma Level",
    "Certificate III & IV Level",
    "Certificate I & II Level",
    "Secondary Education - Years 10 and above",
    "Secondary Education - Years 9 and below",
    "Supplementary Codes",
    "Not stated",
    "Not applicable",
    "Total",
]

ANALYTIC_EDUCATION_ORDER = [
    "Secondary Education - Years 9 and below",
    "Secondary Education - Years 10 and above",
    "Certificate I & II Level",
    "Certificate III & IV Level",
    "Advanced Diploma and Diploma Level",
    "Bachelor Degree Level",
    "Graduate Diploma and Graduate Certificate Level",
    "Postgraduate Degree Level",
]

DISPLAY_EDUCATION_ORDER = [
    "Postgraduate Degree Level",
    "Graduate Diploma and Graduate Certificate Level",
    "Bachelor Degree Level",
    "Advanced Diploma and Diploma Level",
    "Certificate III & IV Level",
    "Certificate I & II Level",
    "Secondary Education - Years 10 and above",
    "Secondary Education - Years 9 and below",
]

EXCLUDED_EDUCATION = {
    "Supplementary Codes",
    "Not stated",
    "Not applicable",
    "Total",
}

INCOME_ORDER = [
    "Negative Income",
    "Nil Income",
    "$1-$149 ($1-$7,799)",
    "$150-$299 ($7,800-$15,599)",
    "$300-$399 ($15,600-$20,799)",
    "$400-$499 ($20,800-$25,999)",
    "$500-$649 ($26,000-$33,799)",
    "$650-$799 ($33,800-$41,599)",
    "$800-$999 ($41,600-$51,999)",
    "$1,000-$1,249 ($52,000-$64,999)",
    "$1,250-$1,499 ($65,000-$77,999)",
    "$1,500-$1,749 ($78,000-$90,999)",
    "$1,750-$1,999 ($91,000-$103,999)",
    "$2,000-$2,999 ($104,000-$155,999)",
    "$3,000-$3,499 ($156,000-$181,999)",
    "$3,500 Or More ($182,000 Or More)",
    "$3,000 Or More ($156,000 Or More)",
    "Not Stated",
]

HARMONISED_INCOME_ORDER = [
    "Negative Income",
    "Nil Income",
    "$1-$149 ($1-$7,799)",
    "$150-$299 ($7,800-$15,599)",
    "$300-$399 ($15,600-$20,799)",
    "$400-$499 ($20,800-$25,999)",
    "$500-$649 ($26,000-$33,799)",
    "$650-$799 ($33,800-$41,599)",
    "$800-$999 ($41,600-$51,999)",
    "$1,000-$1,249 ($52,000-$64,999)",
    "$1,250-$1,499 ($65,000-$77,999)",
    "$1,500-$1,749 ($78,000-$90,999)",
    "$1,750-$1,999 ($91,000-$103,999)",
    "$2,000-$2,999 ($104,000-$155,999)",
    "$3,000 Or More ($156,000 Or More)",
    "Not Stated",
]

EDUCATION_SORT_MAP = {education: index for index, education in enumerate(EDUCATION_ORDER)}
ANALYTIC_EDUCATION_SORT_MAP = {
    education: index for index, education in enumerate(ANALYTIC_EDUCATION_ORDER)
}
DISPLAY_EDUCATION_SORT_MAP = {
    education: index for index, education in enumerate(DISPLAY_EDUCATION_ORDER)
}
HARMONISED_INCOME_SORT_MAP = {
    income: index for index, income in enumerate(HARMONISED_INCOME_ORDER)
}


def ensure_output_dirs() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)


def harmonise_income_bracket(bracket: str) -> str:
    if bracket in {
        "$3,000-$3,499 ($156,000-$181,999)",
        "$3,500 Or More ($182,000 Or More)",
    }:
        return "$3,000 Or More ($156,000 Or More)"
    return bracket


def parse_weekly_midpoint(bracket: str) -> float:
    if pd.isna(bracket):
        return np.nan

    label = str(bracket).strip()
    weekly_label = label.split(" (")[0]

    if weekly_label == "Negative Income":
        return -75.0
    if weekly_label == "Nil Income":
        return 0.0
    if weekly_label == "Not Stated":
        return np.nan

    if "Or More" in weekly_label:
        lower_match = re.search(r"\$([\d,]+)", weekly_label)
        if lower_match:
            lower = float(lower_match.group(1).replace(",", ""))
            return lower + 250.0
        return np.nan

    range_match = re.findall(r"\$([\d,]+)", weekly_label)
    if len(range_match) >= 2:
        lower = float(range_match[0].replace(",", ""))
        upper = float(range_match[1].replace(",", ""))
        return (lower + upper) / 2

    return np.nan


def weighted_median_bracket(group: pd.DataFrame) -> str | None:
    ordered = group.sort_values("harmonised_midpoint")
    total = ordered["count"].sum()
    if total <= 0:
        return None
    cutoff = total / 2
    cumulative = ordered["count"].cumsum()
    median_row = ordered.loc[cumulative >= cutoff].head(1)
    if median_row.empty:
        return None
    return median_row["harmonised_income_bracket"].iloc[0]


def weighted_quantile(values: np.ndarray, weights: np.ndarray, quantile: float) -> float:
    if len(values) == 0:
        return np.nan

    sorter = np.argsort(values)
    values_sorted = values[sorter]
    weights_sorted = weights[sorter]
    cumulative_weights = np.cumsum(weights_sorted)
    cutoff = quantile * weights_sorted.sum()
    return float(values_sorted[np.searchsorted(cumulative_weights, cutoff, side="left")])


def weighted_describe(values: pd.Series, weights: pd.Series) -> dict[str, float]:
    value_array = values.to_numpy(dtype=float)
    weight_array = weights.to_numpy(dtype=float)
    mask = np.isfinite(value_array) & np.isfinite(weight_array) & (weight_array > 0)
    value_array = value_array[mask]
    weight_array = weight_array[mask]

    if len(value_array) == 0:
        return {
            "weighted_count": 0.0,
            "mean": np.nan,
            "std": np.nan,
            "min": np.nan,
            "q1": np.nan,
            "median": np.nan,
            "q3": np.nan,
            "max": np.nan,
        }

    mean = np.average(value_array, weights=weight_array)
    variance = np.average((value_array - mean) ** 2, weights=weight_array)

    return {
        "weighted_count": float(weight_array.sum()),
        "mean": float(mean),
        "std": float(np.sqrt(variance)),
        "min": float(value_array.min()),
        "q1": weighted_quantile(value_array, weight_array, 0.25),
        "median": weighted_quantile(value_array, weight_array, 0.50),
        "q3": weighted_quantile(value_array, weight_array, 0.75),
        "max": float(value_array.max()),
    }


def weighted_pearson(x: pd.Series, y: pd.Series, weights: pd.Series) -> float:
    x_array = x.to_numpy(dtype=float)
    y_array = y.to_numpy(dtype=float)
    w_array = weights.to_numpy(dtype=float)
    mask = np.isfinite(x_array) & np.isfinite(y_array) & np.isfinite(w_array) & (w_array > 0)
    x_array = x_array[mask]
    y_array = y_array[mask]
    w_array = w_array[mask]

    if len(x_array) < 2:
        return np.nan

    x_mean = np.average(x_array, weights=w_array)
    y_mean = np.average(y_array, weights=w_array)
    x_centered = x_array - x_mean
    y_centered = y_array - y_mean
    covariance = np.average(x_centered * y_centered, weights=w_array)
    x_std = np.sqrt(np.average(x_centered**2, weights=w_array))
    y_std = np.sqrt(np.average(y_centered**2, weights=w_array))

    if x_std == 0 or y_std == 0:
        return np.nan

    return float(covariance / (x_std * y_std))


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)

    expected_columns = {"year", "income_bracket", "education", "count"}
    missing_columns = expected_columns.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Dataset is missing required columns: {missing}")

    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["count"] = pd.to_numeric(df["count"], errors="coerce").fillna(0).astype(int)
    df["income_bracket"] = df["income_bracket"].astype(str).str.strip()
    df["education"] = df["education"].astype(str).str.strip()

    df["harmonised_income_bracket"] = df["income_bracket"].map(harmonise_income_bracket)
    df["income_midpoint"] = df["income_bracket"].map(parse_weekly_midpoint)
    df["harmonised_midpoint"] = df["harmonised_income_bracket"].map(parse_weekly_midpoint)

    df["education"] = pd.Categorical(
        df["education"],
        categories=EDUCATION_ORDER,
        ordered=True,
    )
    df["income_bracket"] = pd.Categorical(
        df["income_bracket"],
        categories=INCOME_ORDER,
        ordered=True,
    )
    df["harmonised_income_bracket"] = pd.Categorical(
        df["harmonised_income_bracket"],
        categories=HARMONISED_INCOME_ORDER,
        ordered=True,
    )

    df["is_analytic_education"] = ~df["education"].isin(EXCLUDED_EDUCATION)
    df["education_rank"] = df["education"].map(
        {education: rank + 1 for rank, education in enumerate(ANALYTIC_EDUCATION_ORDER)}
    )
    df["is_stated_income"] = df["harmonised_income_bracket"] != "Not Stated"
    df["weighted_income"] = df["harmonised_midpoint"] * df["count"]
    df["is_high_income"] = df["harmonised_midpoint"] >= 2000
    df["is_low_income"] = df["harmonised_midpoint"] <= 299

    return df


def build_data_quality_table(df: pd.DataFrame) -> pd.DataFrame:
    quality = pd.DataFrame(
        {
            "metric": [
                "rows",
                "columns",
                "year_values",
                "education_categories",
                "income_categories",
                "total_population_count",
                "null_year",
                "null_income_bracket",
                "null_education",
                "null_count",
            ],
            "value": [
                len(df),
                df.shape[1],
                df["year"].nunique(),
                df["education"].nunique(),
                df["income_bracket"].nunique(),
                int(df["count"].sum()),
                int(df["year"].isna().sum()),
                int(df["income_bracket"].isna().sum()),
                int(df["education"].isna().sum()),
                int(df["count"].isna().sum()),
            ],
        }
    )
    return quality


def build_weighted_income_describe(df: pd.DataFrame) -> pd.DataFrame:
    analysis_df = df[df["is_analytic_education"] & df["is_stated_income"]].copy()

    rows = []
    for year, group in analysis_df.groupby("year", observed=True):
        stats = weighted_describe(group["harmonised_midpoint"], group["count"])
        rows.append(
            {
                "year": int(year),
                "weighted_count": round(stats["weighted_count"], 0),
                "mean": round(stats["mean"], 2),
                "std": round(stats["std"], 2),
                "min": round(stats["min"], 2),
                "q1": round(stats["q1"], 2),
                "median": round(stats["median"], 2),
                "q3": round(stats["q3"], 2),
                "max": round(stats["max"], 2),
            }
        )

    return pd.DataFrame(rows).sort_values("year")


def build_variable_overview_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for column in ["year", "income_bracket", "education", "count"]:
        series = df[column]
        rows.append(
            {
                "variable": column,
                "dtype": str(series.dtype),
                "non_missing": int(series.notna().sum()),
                "unique_values": int(series.nunique(dropna=True)),
                "example_values": " | ".join(map(str, series.dropna().astype(str).unique()[:5])),
            }
        )
    return pd.DataFrame(rows)


def build_cleaning_summary_table(df: pd.DataFrame) -> pd.DataFrame:
    analytic_df = df[df["is_analytic_education"] & df["is_stated_income"]]
    summary = pd.DataFrame(
        {
            "step": [
                "Rows in merged dataset",
                "Rows kept for analytic education sample",
                "Rows excluded due to non-analytic education labels",
                "Rows excluded due to unstated income",
                "Distinct original income brackets",
                "Distinct harmonised income brackets",
            ],
            "value": [
                len(df),
                len(analytic_df),
                int((~df["is_analytic_education"]).sum()),
                int((~df["is_stated_income"]).sum()),
                int(df["income_bracket"].nunique()),
                int(df["harmonised_income_bracket"].nunique()),
            ],
        }
    )
    return summary


def build_education_summary(df: pd.DataFrame) -> pd.DataFrame:
    analysis_df = df[df["is_analytic_education"] & df["is_stated_income"]].copy()

    summary = (
        analysis_df.groupby(["year", "education"], observed=True)
        .apply(
            lambda g: pd.Series(
                {
                    "population_count": int(g["count"].sum()),
                    "education_rank": int(g["education_rank"].dropna().iloc[0]),
                    "weighted_mean_income": round(
                        g["weighted_income"].sum() / g["count"].sum(), 2
                    ),
                    "median_income_bracket": weighted_median_bracket(g),
                    "high_income_share_pct": round(
                        100 * g.loc[g["is_high_income"], "count"].sum() / g["count"].sum(),
                        2,
                    ),
                    "low_income_share_pct": round(
                        100 * g.loc[g["is_low_income"], "count"].sum() / g["count"].sum(),
                        2,
                    ),
                }
            ),
            include_groups=False,
        )
        .reset_index()
    )

    summary["education_sort"] = summary["education"].map(DISPLAY_EDUCATION_SORT_MAP)
    summary = summary.sort_values(["year", "weighted_mean_income"], ascending=[True, False])
    summary = summary.drop(columns="education_sort")
    return summary


def build_correlation_table(education_summary: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for year, group in education_summary.groupby("year", observed=True):
        rows.append(
            {
                "sample": str(year),
                "weighted_pearson_rank_mean_income": round(
                    weighted_pearson(
                        group["education_rank"],
                        group["weighted_mean_income"],
                        group["population_count"],
                    ),
                    4,
                ),
                "spearman_rank_mean_income": round(
                    group["education_rank"].corr(
                        group["weighted_mean_income"],
                        method="spearman",
                    ),
                    4,
                ),
                "weighted_pearson_rank_high_income_share": round(
                    weighted_pearson(
                        group["education_rank"],
                        group["high_income_share_pct"],
                        group["population_count"],
                    ),
                    4,
                ),
            }
        )

    rows.append(
        {
            "sample": "Pooled",
            "weighted_pearson_rank_mean_income": round(
                weighted_pearson(
                    education_summary["education_rank"],
                    education_summary["weighted_mean_income"],
                    education_summary["population_count"],
                ),
                4,
            ),
            "spearman_rank_mean_income": round(
                education_summary["education_rank"].corr(
                    education_summary["weighted_mean_income"],
                    method="spearman",
                ),
                4,
            ),
            "weighted_pearson_rank_high_income_share": round(
                weighted_pearson(
                    education_summary["education_rank"],
                    education_summary["high_income_share_pct"],
                    education_summary["population_count"],
                ),
                4,
            ),
        }
    )

    return pd.DataFrame(rows)


def build_year_over_year_change(summary: pd.DataFrame) -> pd.DataFrame:
    pivot = summary.pivot(
        index="education",
        columns="year",
        values=["weighted_mean_income", "high_income_share_pct", "low_income_share_pct"],
    )
    pivot.columns = [f"{metric}_{year}" for metric, year in pivot.columns]
    pivot = pivot.reset_index()

    pivot["mean_income_change_2021_vs_2016"] = (
        pivot["weighted_mean_income_2021"] - pivot["weighted_mean_income_2016"]
    ).round(2)
    pivot["high_income_share_change_pct_points"] = (
        pivot["high_income_share_pct_2021"] - pivot["high_income_share_pct_2016"]
    ).round(2)
    pivot["low_income_share_change_pct_points"] = (
        pivot["low_income_share_pct_2021"] - pivot["low_income_share_pct_2016"]
    ).round(2)

    return pivot.sort_values("mean_income_change_2021_vs_2016", ascending=False)


def build_distribution_table(df: pd.DataFrame) -> pd.DataFrame:
    analysis_df = df[df["is_analytic_education"] & df["is_stated_income"]].copy()

    distribution = (
        analysis_df.groupby(
            ["year", "education", "harmonised_income_bracket"],
            observed=True,
        )["count"]
        .sum()
        .reset_index()
    )

    totals = distribution.groupby(["year", "education"], observed=True)["count"].transform("sum")
    distribution["share_pct"] = (100 * distribution["count"] / totals).round(2)

    distribution["education_sort"] = distribution["education"].map(ANALYTIC_EDUCATION_SORT_MAP)
    distribution["income_sort"] = distribution["harmonised_income_bracket"].map(
        HARMONISED_INCOME_SORT_MAP
    )
    distribution = distribution.sort_values(
        ["year", "education_sort", "income_sort"]
    )
    distribution = distribution.drop(columns=["education_sort", "income_sort"])
    return distribution


def build_top_bracket_summary(df: pd.DataFrame) -> pd.DataFrame:
    top_brackets = {
        "$2,000-$2,999 ($104,000-$155,999)",
        "$3,000 Or More ($156,000 Or More)",
    }
    analysis_df = df[df["is_analytic_education"] & df["is_stated_income"]].copy()
    analysis_df["is_top_two_brackets"] = analysis_df["harmonised_income_bracket"].isin(top_brackets)

    top_summary = (
        analysis_df.groupby(["year", "education"], observed=True)
        .apply(
            lambda g: pd.Series(
                {
                    "top_two_brackets_share_pct": round(
                        100
                        * g.loc[g["is_top_two_brackets"], "count"].sum()
                        / g["count"].sum(),
                        2,
                    )
                }
            ),
            include_groups=False,
        )
        .reset_index()
    )

    top_summary["education_sort"] = top_summary["education"].map(ANALYTIC_EDUCATION_SORT_MAP)
    top_summary = top_summary.sort_values(
        ["year", "top_two_brackets_share_pct"],
        ascending=[True, False],
    )
    return top_summary.drop(columns="education_sort")


def save_tables(
    quality: pd.DataFrame,
    variable_overview: pd.DataFrame,
    cleaning_summary: pd.DataFrame,
    weighted_describe_table: pd.DataFrame,
    education_summary: pd.DataFrame,
    correlation_table: pd.DataFrame,
    yoy_change: pd.DataFrame,
    distribution: pd.DataFrame,
    top_summary: pd.DataFrame,
) -> None:
    quality.to_csv(TABLES_DIR / "data_quality_summary.csv", index=False)
    variable_overview.to_csv(TABLES_DIR / "variable_overview.csv", index=False)
    cleaning_summary.to_csv(TABLES_DIR / "cleaning_summary.csv", index=False)
    weighted_describe_table.to_csv(TABLES_DIR / "weighted_income_describe_by_year.csv", index=False)
    education_summary.to_csv(TABLES_DIR / "education_income_summary.csv", index=False)
    correlation_table.to_csv(TABLES_DIR / "correlation_summary.csv", index=False)
    yoy_change.to_csv(TABLES_DIR / "education_year_over_year_change.csv", index=False)
    distribution.to_csv(TABLES_DIR / "income_distribution_by_education.csv", index=False)
    top_summary.to_csv(TABLES_DIR / "top_income_bracket_summary.csv", index=False)


def plot_population_by_education(education_summary: pd.DataFrame) -> None:
    plot_df = education_summary.copy()
    plot_df["education_sort"] = plot_df["education"].map(DISPLAY_EDUCATION_SORT_MAP)
    plot_df = plot_df.sort_values(["year", "education_sort"])

    plt.figure(figsize=(12, 7))
    sns.barplot(
        data=plot_df,
        x="population_count",
        y="education",
        hue="year",
        orient="h",
    )
    plt.title("Population Count by Education Level and Census Year")
    plt.xlabel("Population count")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "population_by_education_year.png", dpi=300)
    plt.close()


def plot_weighted_boxplot_by_year(df: pd.DataFrame) -> None:
    analysis_df = df[df["is_analytic_education"] & df["is_stated_income"]].copy()
    stats = []

    for year, group in analysis_df.groupby("year", observed=True):
        describe = weighted_describe(group["harmonised_midpoint"], group["count"])
        iqr = describe["q3"] - describe["q1"]
        whisker_low = max(describe["min"], describe["q1"] - 1.5 * iqr)
        whisker_high = min(describe["max"], describe["q3"] + 1.5 * iqr)
        stats.append(
            {
                "label": str(year),
                "med": describe["median"],
                "q1": describe["q1"],
                "q3": describe["q3"],
                "whislo": whisker_low,
                "whishi": whisker_high,
                "fliers": [],
            }
        )

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bxp(stats, showfliers=False, patch_artist=True)
    for patch in ax.patches:
        patch.set_facecolor("#5B7DB1")
        patch.set_alpha(0.75)
    ax.set_title("Tukey-Style Weighted Boxplot of Weekly Income by Year")
    ax.set_xlabel("Census year")
    ax.set_ylabel("Estimated weekly income midpoint")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "weighted_income_boxplot_by_year.png", dpi=300)
    plt.close(fig)


def plot_weighted_mean_income(education_summary: pd.DataFrame) -> None:
    plot_df = education_summary.copy()
    plot_df["education_sort"] = plot_df["education"].map(DISPLAY_EDUCATION_SORT_MAP)
    plot_df = plot_df.sort_values(["year", "education_sort"])

    plt.figure(figsize=(12, 7))
    sns.barplot(
        data=plot_df,
        x="weighted_mean_income",
        y="education",
        hue="year",
        orient="h",
    )
    plt.title("Weighted Mean Weekly Income by Education Level")
    plt.xlabel("Estimated weekly income midpoint")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "weighted_mean_income_by_education.png", dpi=300)
    plt.close()


def plot_first_order_effect(education_summary: pd.DataFrame) -> None:
    plot_df = education_summary.sort_values(["year", "education_rank"])

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(
        data=plot_df,
        x="education_rank",
        y="weighted_mean_income",
        hue="year",
        marker="o",
        ax=ax,
    )
    ax.set_title("First-Order Education-Income Gradient")
    ax.set_xlabel("Education rank from lower to higher attainment")
    ax.set_ylabel("Weighted mean weekly income")
    ax.set_xticks(range(1, len(ANALYTIC_EDUCATION_ORDER) + 1))
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "first_order_effect_education_income.png", dpi=300)
    plt.close(fig)


def plot_income_ecdf_by_year(df: pd.DataFrame) -> None:
    analysis_df = df[df["is_analytic_education"] & df["is_stated_income"]].copy()
    grouped = (
        analysis_df.groupby(["year", "harmonised_midpoint"], observed=True)["count"]
        .sum()
        .reset_index()
        .sort_values(["year", "harmonised_midpoint"])
    )
    grouped["cdf"] = grouped.groupby("year", observed=True)["count"].cumsum()
    totals = grouped.groupby("year", observed=True)["count"].transform("sum")
    grouped["cdf"] = grouped["cdf"] / totals

    fig, ax = plt.subplots(figsize=(10, 5.5))
    sns.lineplot(data=grouped, x="harmonised_midpoint", y="cdf", hue="year", marker="o", ax=ax)
    ax.set_title("Empirical CDF of Estimated Weekly Income by Year")
    ax.set_xlabel("Estimated weekly income midpoint")
    ax.set_ylabel("Cumulative share")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "income_ecdf_by_year.png", dpi=300)
    plt.close(fig)


def plot_income_distribution_by_year(distribution: pd.DataFrame, year: int) -> None:
    plot_df = distribution[distribution["year"] == year].copy()
    heatmap_df = plot_df.pivot(
        index="education",
        columns="harmonised_income_bracket",
        values="share_pct",
    ).reindex(index=DISPLAY_EDUCATION_ORDER, columns=HARMONISED_INCOME_ORDER[:-1])

    plt.figure(figsize=(14, 6))
    sns.heatmap(heatmap_df, cmap="YlGnBu", linewidths=0.5, annot=False)
    plt.title(f"Income Distribution by Education Level ({year})")
    plt.xlabel("Income bracket")
    plt.ylabel("")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / f"income_distribution_heatmap_{year}.png", dpi=300)
    plt.close()


def plot_income_distribution_change_heatmap(distribution: pd.DataFrame) -> None:
    pivot = distribution.pivot_table(
        index=["education", "harmonised_income_bracket"],
        columns="year",
        values="share_pct",
        aggfunc="sum",
    ).reset_index()
    pivot["share_change_pct_points"] = pivot[2021] - pivot[2016]
    heatmap_df = pivot.pivot(
        index="education",
        columns="harmonised_income_bracket",
        values="share_change_pct_points",
    ).reindex(index=DISPLAY_EDUCATION_ORDER, columns=HARMONISED_INCOME_ORDER[:-1])

    plt.figure(figsize=(14, 6))
    sns.heatmap(heatmap_df, cmap="RdBu_r", center=0, linewidths=0.5, annot=False)
    plt.title("Change in Income Distribution Share, 2021 vs 2016")
    plt.xlabel("Income bracket")
    plt.ylabel("")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "income_distribution_change_heatmap.png", dpi=300)
    plt.close()


def plot_year_over_year_change(yoy_change: pd.DataFrame) -> None:
    plot_df = yoy_change.sort_values("mean_income_change_2021_vs_2016", ascending=True)

    plt.figure(figsize=(12, 7))
    sns.barplot(
        data=plot_df,
        x="mean_income_change_2021_vs_2016",
        y="education",
        hue="education",
        palette="viridis",
        orient="h",
        legend=False,
    )
    plt.title("Change in Weighted Mean Weekly Income (2021 vs 2016)")
    plt.xlabel("Change in estimated weekly income midpoint")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "weighted_mean_income_change.png", dpi=300)
    plt.close()


def plot_overall_income_distribution(df: pd.DataFrame) -> None:
    overall = (
        df[df["is_analytic_education"] & df["is_stated_income"]]
        .groupby(["year", "harmonised_income_bracket"], observed=True)["count"]
        .sum()
        .reset_index()
    )
    totals = overall.groupby("year", observed=True)["count"].transform("sum")
    overall["share_pct"] = 100 * overall["count"] / totals

    plt.figure(figsize=(13, 6))
    sns.barplot(
        data=overall,
        x="harmonised_income_bracket",
        y="share_pct",
        hue="year",
    )
    plt.title("Overall Income Distribution Across Census Years")
    plt.xlabel("Income bracket")
    plt.ylabel("Share of population (%)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "overall_income_distribution_by_year.png", dpi=300)
    plt.close()


def plot_top_income_share_by_education(top_summary: pd.DataFrame) -> None:
    plot_df = top_summary.copy()
    plot_df["education_sort"] = plot_df["education"].map(DISPLAY_EDUCATION_SORT_MAP)
    plot_df = plot_df.sort_values(["year", "education_sort"])

    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(
        data=plot_df,
        x="top_two_brackets_share_pct",
        y="education",
        hue="year",
        orient="h",
        ax=ax,
    )
    ax.set_title("Share in Top Two Income Brackets by Education")
    ax.set_xlabel("Share of group in top two brackets (%)")
    ax.set_ylabel("")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "top_income_share_by_education.png", dpi=300)
    plt.close(fig)


def write_report(
    df: pd.DataFrame,
    variable_overview: pd.DataFrame,
    cleaning_summary: pd.DataFrame,
    weighted_describe_table: pd.DataFrame,
    education_summary: pd.DataFrame,
    correlation_table: pd.DataFrame,
    yoy_change: pd.DataFrame,
    top_summary: pd.DataFrame,
) -> None:
    analysis_df = df[df["is_analytic_education"] & df["is_stated_income"]]
    total_population = int(analysis_df["count"].sum())
    years = sorted(analysis_df["year"].dropna().unique().tolist())

    best_2016 = (
        education_summary[education_summary["year"] == 2016]
        .sort_values("weighted_mean_income", ascending=False)
        .iloc[0]
    )
    best_2021 = (
        education_summary[education_summary["year"] == 2021]
        .sort_values("weighted_mean_income", ascending=False)
        .iloc[0]
    )
    largest_gain = yoy_change.iloc[0]
    smallest_gain = yoy_change.iloc[-1]
    top_2021 = (
        top_summary[top_summary["year"] == 2021]
        .sort_values("top_two_brackets_share_pct", ascending=False)
        .iloc[0]
    )
    describe_2016 = weighted_describe_table[weighted_describe_table["year"] == 2016].iloc[0]
    describe_2021 = weighted_describe_table[weighted_describe_table["year"] == 2021].iloc[0]
    pooled_corr = correlation_table[correlation_table["sample"] == "Pooled"].iloc[0]
    corr_2016 = correlation_table[correlation_table["sample"] == "2016"].iloc[0]
    corr_2021 = correlation_table[correlation_table["sample"] == "2021"].iloc[0]
    income_categories = int(
        variable_overview.loc[
            variable_overview["variable"] == "income_bracket",
            "unique_values",
        ].iloc[0]
    )
    education_categories = int(
        variable_overview.loc[
            variable_overview["variable"] == "education",
            "unique_values",
        ].iloc[0]
    )
    excluded_education_rows = int(
        cleaning_summary.loc[
            cleaning_summary["step"] == "Rows excluded due to non-analytic education labels",
            "value",
        ].iloc[0]
    )
    excluded_unstated_income_rows = int(
        cleaning_summary.loc[
            cleaning_summary["step"] == "Rows excluded due to unstated income",
            "value",
        ].iloc[0]
    )

    report = f"""# Exploratory Data Analysis Report

## Scope

This report analyses `data/clean/merged_2016_2021.csv`, which contains counts of Australian males by census year,
income bracket, and highest educational attainment. The substantive analysis focuses on the eight meaningful education
groups rather than administrative categories such as `Total`, `Not stated`, and `Supplementary Codes`.

Two preparation choices are especially important for interpretation. First, `Not Stated` income rows are excluded from
numeric income summaries so that estimated means and medians reflect observed brackets. Second, the split 2021 top-income
categories are recombined into a single `$3,000 Or More ($156,000 Or More)` bracket so that the 2016 and 2021 distributions
are directly comparable.

## Dataset Snapshot

- Census years analysed: {", ".join(str(year) for year in years)}
- Rows in merged dataset: {len(df):,}
- Rows in analytic sample: {len(analysis_df):,}
- Total weighted population count in analytic sample: {total_population:,}
- Education groups analysed: {len(ANALYTIC_EDUCATION_ORDER)}

## Basic Description of Data Characteristics

The data are stored in long format, with each row representing a `year x income_bracket x education` cell and `count`
recording the number of people in that cell. In the raw merged file there are **{income_categories}** income categories
and **{education_categories}** education categories, which is consistent with the ABS extraction once summary labels are included.

The cleaning and preparation steps materially improve comparability. A total of **{excluded_education_rows}** rows are excluded
from the core education comparison because they correspond to non-substantive labels such as `Total`, `Not applicable`,
`Not stated`, and `Supplementary Codes`. A further **{excluded_unstated_income_rows}** rows are excluded from numeric income
summaries because the income value itself is missing. These choices ensure that the main comparisons describe real attainment
groups and stated income outcomes rather than administrative totals or missing-information categories.

## Univariate EDA

The univariate analysis shows that the data are highly unbalanced across cells, so weighting by population count is necessary
throughout. This is an important feature of the dataset rather than a minor detail, because small categories would otherwise
have the same influence as very large ones.

The estimated income distribution also shifts upward between censuses. The weighted median rises from **{describe_2016["median"]:.2f}**
in 2016 to **{describe_2021["median"]:.2f}** in 2021, while the interquartile range moves from **{describe_2016["q1"]:.2f}-{describe_2016["q3"]:.2f}**
to **{describe_2021["q1"]:.2f}-{describe_2021["q3"]:.2f}**. The weighted boxplot and ECDF confirm that the 2021 distribution lies broadly
to the right of the 2016 distribution, indicating a general upward shift rather than a change confined to the upper tail.

## Variation Between Variables

The main source of variation in the data is across education groups. Lower-attainment categories are more concentrated in lower
income brackets, while higher-attainment categories are much more represented in the upper brackets. There is also clear variation
across time, with the overall income distribution in 2021 shifted upward relative to 2016.

This variation is not limited to simple differences in means. The distribution heatmaps show that education is associated with
changes in where the full income distribution sits, especially in the upper-income brackets. This matters because an analysis
focused only on average income would miss an important part of the structure in the data.

## Education and Income Relationships

This section addresses the core first-order question: do higher education categories line up with higher income?

1. The highest estimated weekly income in 2016 was for **{best_2016["education"]}**
   at approximately **{best_2016["weighted_mean_income"]:.2f}**.
2. The highest estimated weekly income in 2021 was again **{best_2021["education"]}**
   at approximately **{best_2021["weighted_mean_income"]:.2f}**.
3. The largest rise in weighted mean weekly income between 2016 and 2021 was for
   **{largest_gain["education"]}** with an increase of **{largest_gain["mean_income_change_2021_vs_2016"]:.2f}**.
4. The smallest rise in weighted mean weekly income between 2016 and 2021 was for
   **{smallest_gain["education"]}** with an increase of **{smallest_gain["mean_income_change_2021_vs_2016"]:.2f}**.
5. In 2021, the education group with the largest share of people in the top two income brackets
   (`$2,000-$2,999` and `$3,000+`) was **{top_2021["education"]}**
   at **{top_2021["top_two_brackets_share_pct"]:.2f}%**.

The first-order education-income effect is strong in both years.

- Weighted Pearson correlation between education rank and weighted mean income is **{corr_2016["weighted_pearson_rank_mean_income"]:.4f}** in 2016.
- Weighted Pearson correlation between education rank and weighted mean income is **{corr_2021["weighted_pearson_rank_mean_income"]:.4f}** in 2021.
- The pooled weighted Pearson correlation is **{pooled_corr["weighted_pearson_rank_mean_income"]:.4f}**.

Taken together, these results indicate a clear and persistent education-income gradient. Education should therefore remain central
in any later model of income outcomes.

## Modelling Implications

This EDA highlights several points that should shape later modelling decisions.

1. **Transformation choice matters:** income is observed as ordered brackets rather than raw dollars, so converting brackets to midpoints is a useful approximation but not a perfect continuous measure.
   Later models should therefore be interpreted as using an income proxy, especially at the top open-ended bracket.
2. **No clear Simpson's paradox reversal appears here:** the correlation stays positive in 2016, 2021, and the pooled sample.
   Pooling does not reverse the headline relationship, but year should still be controlled for because the whole income distribution shifts upward from 2016 to 2021.
3. **Weighting is essential:** rare groups such as `Certificate I & II Level` have very small counts compared with major categories.
   Unweighted row-level models would therefore distort influence across groups.
4. **Means are not the whole story:** the distribution heatmaps and top-income-share charts show that education changes where the whole distribution sits, not just the average.
   Distribution-aware modelling approaches may therefore be more informative than a single mean-based specification.
5. **Ordinal structure is real:** both education and income brackets have natural ordering.
   Rank-based checks, ordered models, or carefully chosen monotonic specifications may therefore be sensible next steps.

## Valuable Questions This Data Can Answer

This dataset is well suited to answering several substantive questions.

1. How strongly is educational attainment associated with weekly personal income for Australian males?
   This is the core question addressed by the first-order gradient and correlation results.
2. Did the education-income relationship strengthen, weaken, or stay broadly stable between 2016 and 2021?
   This can be studied using the year-by-year summaries and the year-over-year change tables.
3. Which education groups experienced the largest upward shift in income between censuses?
   This is directly answered by the weighted mean change and distribution-shift outputs.
4. Are differences across education groups mostly about average income, or do they affect the full distribution?
   This is what the heatmaps and top-income-share plots help answer.
5. Which groups remain concentrated in low-income brackets, and which groups are most represented in top-income brackets?
   This can inform targeted interpretation about inequality across attainment levels.

## Files Produced

### Tables

- `outputs/eda/tables/data_quality_summary.csv`
- `outputs/eda/tables/variable_overview.csv`
- `outputs/eda/tables/cleaning_summary.csv`
- `outputs/eda/tables/weighted_income_describe_by_year.csv`
- `outputs/eda/tables/education_income_summary.csv`
- `outputs/eda/tables/correlation_summary.csv`
- `outputs/eda/tables/education_year_over_year_change.csv`
- `outputs/eda/tables/income_distribution_by_education.csv`
- `outputs/eda/tables/top_income_bracket_summary.csv`

### Figures

- `outputs/eda/figures/population_by_education_year.png`
- `outputs/eda/figures/weighted_income_boxplot_by_year.png`
- `outputs/eda/figures/income_ecdf_by_year.png`
- `outputs/eda/figures/weighted_mean_income_by_education.png`
- `outputs/eda/figures/first_order_effect_education_income.png`
- `outputs/eda/figures/income_distribution_heatmap_2016.png`
- `outputs/eda/figures/income_distribution_heatmap_2021.png`
- `outputs/eda/figures/income_distribution_change_heatmap.png`
- `outputs/eda/figures/weighted_mean_income_change.png`
- `outputs/eda/figures/overall_income_distribution_by_year.png`
- `outputs/eda/figures/top_income_share_by_education.png`
"""

    REPORT_PATH.write_text(report, encoding="utf-8")


def main() -> None:
    ensure_output_dirs()
    sns.set_theme(style="whitegrid", palette="deep")

    df = load_data()
    quality = build_data_quality_table(df)
    variable_overview = build_variable_overview_table(df)
    cleaning_summary = build_cleaning_summary_table(df)
    weighted_describe_table = build_weighted_income_describe(df)
    education_summary = build_education_summary(df)
    correlation_table = build_correlation_table(education_summary)
    yoy_change = build_year_over_year_change(education_summary)
    distribution = build_distribution_table(df)
    top_summary = build_top_bracket_summary(df)

    save_tables(
        quality,
        variable_overview,
        cleaning_summary,
        weighted_describe_table,
        education_summary,
        correlation_table,
        yoy_change,
        distribution,
        top_summary,
    )

    plot_population_by_education(education_summary)
    plot_weighted_boxplot_by_year(df)
    plot_income_ecdf_by_year(df)
    plot_weighted_mean_income(education_summary)
    plot_first_order_effect(education_summary)
    plot_income_distribution_by_year(distribution, 2016)
    plot_income_distribution_by_year(distribution, 2021)
    plot_income_distribution_change_heatmap(distribution)
    plot_year_over_year_change(yoy_change)
    plot_overall_income_distribution(df)
    plot_top_income_share_by_education(top_summary)

    write_report(
        df,
        variable_overview,
        cleaning_summary,
        weighted_describe_table,
        education_summary,
        correlation_table,
        yoy_change,
        top_summary,
    )

    print("EDA complete.")
    print(f"Report: {REPORT_PATH}")
    print(f"Tables: {TABLES_DIR}")
    print(f"Figures: {FIGURES_DIR}")


if __name__ == "__main__":
    main()

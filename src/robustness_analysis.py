from pathlib import Path
import re
from typing import Callable, Dict, List, Optional

import numpy as np
import pandas as pd
import statsmodels.api as sm

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

EXCLUDED_EDUCATION = {
    "Supplementary Codes",
    "Not stated",
    "Not applicable",
    "Total",
}

TOP_INCOME_BRACKET = "$3,000 Or More ($156,000 Or More)"
HARMONISED_TOP_INCOME_BRACKETS = {
    "$3,000-$3,499 ($156,000-$181,999)",
    "$3,500 Or More ($182,000 Or More)",
}

EDUCATION_RANK_MAP = {
    education: rank + 1 for rank, education in enumerate(ANALYTIC_EDUCATION_ORDER)
}


def harmonise_income_bracket(bracket: Optional[str]) -> Optional[str]:
    if pd.isna(bracket):
        return None
    if bracket in HARMONISED_TOP_INCOME_BRACKETS:
        return TOP_INCOME_BRACKET
    return bracket


def parse_weekly_midpoint(bracket: Optional[str]) -> float:
    if pd.isna(bracket) or bracket is None:
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
        return (lower + upper) / 2.0

    return np.nan


def load_clean_data(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["harmonised_income_bracket"] = df["income_bracket"].map(harmonise_income_bracket)
    df["income_midpoint"] = df["income_bracket"].map(parse_weekly_midpoint)
    df["harmonised_midpoint"] = df["harmonised_income_bracket"].map(parse_weekly_midpoint)
    df["is_analytic_education"] = ~df["education"].isin(EXCLUDED_EDUCATION)
    df["education_rank"] = df["education"].map(EDUCATION_RANK_MAP)
    df["is_stated_income"] = df["harmonised_income_bracket"] != "Not Stated"
    df["weighted_income"] = df["harmonised_midpoint"] * df["count"]
    return df


def build_regression_dataset(
    df: pd.DataFrame,
    sample_filter: Optional[Callable[[pd.DataFrame], pd.Series]] = None,
    outcome_transform: Optional[Callable[[pd.Series], pd.Series]] = None,
) -> pd.DataFrame:
    analytic_df = df[df["is_analytic_education"] & df["is_stated_income"]].copy()
    if sample_filter is not None:
        analytic_df = analytic_df[sample_filter(analytic_df)].copy()

    grouped = (
        analytic_df.groupby(["year", "education"], observed=True)
        .agg(
            total_count=("count", "sum"),
            weighted_income=("weighted_income", "sum"),
            education_rank=("education_rank", "first"),
        )
        .reset_index()
    )
    grouped["weighted_mean_income"] = grouped["weighted_income"] / grouped["total_count"]
    grouped["year_2021"] = (grouped["year"] == 2021).astype(int)
    if outcome_transform is not None:
        grouped["outcome"] = outcome_transform(grouped["weighted_mean_income"])
    else:
        grouped["outcome"] = grouped["weighted_mean_income"]
    return grouped


def estimate_wls(
    reg_df: pd.DataFrame,
    include_year: bool = True,
    robust: bool = False,
    weighted: bool = True,
) -> sm.regression.linear_model.RegressionResultsWrapper:
    X = reg_df[["education_rank"]].copy()
    if include_year:
        X["year_2021"] = reg_df["year_2021"]
    X = sm.add_constant(X)
    y = reg_df["outcome"]
    if weighted:
        weights = reg_df["total_count"]
        model = sm.WLS(y, X, weights=weights)
    else:
        model = sm.OLS(y, X)
    results = model.fit()
    if robust:
        return results.get_robustcov_results(cov_type="HC0")
    return results


def extract_parameter(results: sm.regression.linear_model.RegressionResultsWrapper, term: str) -> float:
    if hasattr(results.params, "get"):
        return float(results.params.get(term))

    names = list(results.model.exog_names)
    if term not in names:
        raise KeyError(f"Term '{term}' not found in model exog names: {names}")
    return float(results.params[names.index(term)])


def build_robustness_table(df: pd.DataFrame) -> pd.DataFrame:
    checks = [
        {
            "label": "Main",
            "filter": None,
            "include_year": True,
            "outcome_transform": None,
            "robust": False,
            "weighted": True,
            "note": "WLS on weighted mean income with year control.",
        },
        {
            "label": "No controls",
            "filter": None,
            "include_year": False,
            "outcome_transform": None,
            "robust": False,
            "weighted": True,
            "note": "Test the association without the year control.",
        },
        {
            "label": "Drop top bracket",
            "filter": lambda d: d["harmonised_income_bracket"] != TOP_INCOME_BRACKET,
            "include_year": True,
            "outcome_transform": None,
            "robust": False,
            "weighted": True,
            "note": "Exclude the top open-ended income bracket.",
        },
        {
            "label": "IHS outcome",
            "filter": None,
            "include_year": True,
            "outcome_transform": np.arcsinh,
            "robust": False,
            "weighted": True,
            "note": "Use inverse-hyperbolic-sine transformation of income.",
        },
        {
            "label": "Log outcome",
            "filter": lambda d: ~d["harmonised_income_bracket"].isin(["Negative Income", "Nil Income"]),
            "include_year": True,
            "outcome_transform": np.log,
            "robust": False,
            "weighted": True,
            "note": "Use natural log transformation of income (excluding zero/negative).",
        },
        {
            "label": "2021 only",
            "filter": lambda d: d["year"] == 2021,
            "include_year": False,
            "outcome_transform": None,
            "robust": False,
            "weighted": True,
            "note": "Check the association inside the 2021 sample only.",
        },
        {
            "label": "2016 only",
            "filter": lambda d: d["year"] == 2016,
            "include_year": False,
            "outcome_transform": None,
            "robust": False,
            "weighted": True,
            "note": "Check the association inside the 2016 sample only.",
        },
        {
            "label": "HC0 SE",
            "filter": None,
            "include_year": True,
            "outcome_transform": None,
            "robust": True,
            "weighted": True,
            "note": "Same model with heteroskedasticity-robust standard errors.",
        },
        {
            "label": "Unweighted OLS",
            "filter": None,
            "include_year": True,
            "outcome_transform": None,
            "robust": False,
            "weighted": False,
            "note": "Use OLS without weighting by sample size.",
        },
        {
            "label": "Exclude negative income",
            "filter": lambda d: d["harmonised_income_bracket"] != "Negative Income",
            "include_year": True,
            "outcome_transform": None,
            "robust": False,
            "weighted": True,
            "note": "Exclude observations with negative income.",
        },
    ]

    summary_rows: Dict[str, Dict[str, object]] = {}
    for check in checks:
        reg_df = build_regression_dataset(
            df,
            sample_filter=check["filter"],
            outcome_transform=check["outcome_transform"],
        )
        results = estimate_wls(
            reg_df,
            include_year=check["include_year"],
            robust=check["robust"],
            weighted=check["weighted"],
        )

        N = int(reg_df["total_count"].sum())
        education_coef = extract_parameter(results, "education_rank")
        if hasattr(results.bse, "get"):
            education_se = float(results.bse.get("education_rank"))
        else:
            education_se = float(results.bse[list(results.model.exog_names).index("education_rank")])
        education_p = float(results.pvalues["education_rank"]) if hasattr(results.pvalues, "get") else float(results.pvalues[list(results.model.exog_names).index("education_rank")])
        year_coef = extract_parameter(results, "year_2021") if check["include_year"] else np.nan
        if check["include_year"]:
            if hasattr(results.bse, "get"):
                year_se = float(results.bse.get("year_2021"))
            else:
                year_se = float(results.bse[list(results.model.exog_names).index("year_2021")])
        else:
            year_se = np.nan

        summary_rows.setdefault("N", {})[check["label"]] = N
        summary_rows.setdefault("education_rank coef", {})[check["label"]] = education_coef
        summary_rows.setdefault("education_rank se", {})[check["label"]] = education_se
        summary_rows.setdefault("education_rank p", {})[check["label"]] = education_p
        summary_rows.setdefault("year_2021 coef", {})[check["label"]] = year_coef
        summary_rows.setdefault("year_2021 se", {})[check["label"]] = year_se
        summary_rows.setdefault("notes", {})[check["label"]] = check["note"]

    table = pd.DataFrame(summary_rows).T
    return table


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    clean_path = project_root / "data" / "clean" / "merged_2016_2021.csv"
    output_dir = project_root / "outputs" / "analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    df = load_clean_data(clean_path)
    table = build_robustness_table(df)
    table.to_csv(output_dir / "robustness_table.csv")
    print(f"Saved robustness summary to {output_dir / 'robustness_table.csv'}")


if __name__ == "__main__":
    main()

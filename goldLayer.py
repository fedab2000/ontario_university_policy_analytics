import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# Gold Layer Creation
# Project: Ontario University Policy Analytics Platform
#
# Purpose:
# The Gold layer converts the cleaned Silver dataset into
# business-ready and executive-ready analytics outputs.
#
# Gold outputs are designed for:
# - executive dashboards
# - policy briefing notes
# - funding analysis
# - enrolment trend analysis
# - scenario modelling
# ============================================================


# -----------------------------
# 1. Define project folders
# -----------------------------
base_path = Path("ontario_university_policy_analytics")

silver_path = base_path / "data" / "silver"
gold_path = base_path / "data" / "gold"

gold_path.mkdir(parents=True, exist_ok=True)


# -----------------------------
# 2. Load Silver dataset
# -----------------------------
silver = pd.read_csv(silver_path / "silver_university_financials.csv")


# ============================================================
# GOLD TABLE 1: EXECUTIVE KPI SUMMARY
# ============================================================
# This table summarizes the sector by year.
# It is useful for executive reporting and policy briefings.
# ============================================================

gold_sector_kpis = (
    silver
    .groupby("year")
    .agg(
        total_domestic_enrolment=("domestic_enrolment", "sum"),
        total_international_enrolment=("international_enrolment", "sum"),
        total_enrolment=("total_enrolment", "sum"),
        total_tuition_revenue=("total_tuition_revenue", "sum"),
        total_operating_grant=("operating_grant", "sum"),
        total_special_purpose_grants=("special_purpose_grants", "sum"),
        avg_funding_per_student=("funding_per_student", "mean"),
        avg_international_share=("international_share", "mean"),
        avg_grant_dependency_ratio=("grant_dependency_ratio", "mean")
    )
    .reset_index()
)

# Create additional executive KPIs.
gold_sector_kpis["sector_international_share"] = (
    gold_sector_kpis["total_international_enrolment"] /
    gold_sector_kpis["total_enrolment"]
)

gold_sector_kpis["sector_grant_dependency_ratio"] = (
    gold_sector_kpis["total_operating_grant"] /
    (
        gold_sector_kpis["total_operating_grant"] +
        gold_sector_kpis["total_tuition_revenue"]
    )
)

gold_sector_kpis["sector_funding_per_student"] = (
    gold_sector_kpis["total_operating_grant"] /
    gold_sector_kpis["total_enrolment"]
)

gold_sector_kpis = gold_sector_kpis.round(4)

gold_sector_kpis.to_csv(
    gold_path / "gold_sector_kpi_summary.csv",
    index=False
)


# ============================================================
# GOLD TABLE 2: UNIVERSITY KPI SUMMARY
# ============================================================
# This table summarizes each university across the full period.
# It is useful for comparing institutions.
# ============================================================

gold_university_kpis = (
    silver
    .groupby(["university", "university_profile"])
    .agg(
        avg_total_enrolment=("total_enrolment", "mean"),
        latest_total_enrolment=("total_enrolment", "last"),
        avg_international_share=("international_share", "mean"),
        latest_international_share=("international_share", "last"),
        avg_funding_per_student=("funding_per_student", "mean"),
        latest_funding_per_student=("funding_per_student", "last"),
        avg_grant_dependency_ratio=("grant_dependency_ratio", "mean"),
        latest_grant_dependency_ratio=("grant_dependency_ratio", "last"),
        avg_total_tuition_revenue=("total_tuition_revenue", "mean"),
        latest_total_tuition_revenue=("total_tuition_revenue", "last"),
        avg_operating_grant=("operating_grant", "mean"),
        latest_operating_grant=("operating_grant", "last")
    )
    .reset_index()
)

gold_university_kpis = gold_university_kpis.round(2)

gold_university_kpis.to_csv(
    gold_path / "gold_university_kpi_summary.csv",
    index=False
)


# ============================================================
# GOLD TABLE 3: POLICY RISK SUMMARY
# ============================================================
# This table highlights universities with higher exposure to
# policy risks, such as international enrolment pressure or
# high dependency on operating grants.
# ============================================================

latest_year = silver["year"].max()

latest_data = silver[silver["year"] == latest_year].copy()

gold_policy_risk = latest_data[
    [
        "university",
        "university_profile",
        "year",
        "total_enrolment",
        "international_share",
        "grant_dependency_ratio",
        "international_tuition_dependency_ratio",
        "funding_per_student",
        "high_international_exposure_flag",
        "high_grant_dependency_flag"
    ]
].copy()

# Create a simple combined policy risk score.
# This is not meant to be a formal risk model.
# It is an interpretable executive-facing score.
gold_policy_risk["policy_risk_score"] = (
    gold_policy_risk["international_share"] * 0.45 +
    gold_policy_risk["international_tuition_dependency_ratio"] * 0.35 +
    gold_policy_risk["grant_dependency_ratio"] * 0.20
)

gold_policy_risk["policy_risk_level"] = pd.cut(
    gold_policy_risk["policy_risk_score"],
    bins=[-np.inf, 0.25, 0.40, np.inf],
    labels=["Low", "Medium", "High"]
)

gold_policy_risk = gold_policy_risk.sort_values(
    "policy_risk_score",
    ascending=False
)

gold_policy_risk = gold_policy_risk.round(4)

gold_policy_risk.to_csv(
    gold_path / "gold_policy_risk_summary.csv",
    index=False
)


# ============================================================
# GOLD TABLE 4: INTERNATIONAL ENROLMENT SCENARIO
# ============================================================
# This scenario estimates the financial impact of a 10% decline
# in international enrolment.
#
# This is highly relevant for policy and university financial
# planning because many institutions rely on international tuition.
# ============================================================

scenario = latest_data.copy()

scenario["scenario_name"] = "10_percent_international_enrolment_decline"

scenario["scenario_international_enrolment"] = (
    scenario["international_enrolment"] * 0.90
)

scenario["scenario_international_tuition_revenue"] = (
    scenario["scenario_international_enrolment"] *
    scenario["avg_international_tuition"]
)

scenario["baseline_total_revenue"] = (
    scenario["total_tuition_revenue"] +
    scenario["operating_grant"] +
    scenario["special_purpose_grants"]
)

scenario["scenario_total_revenue"] = (
    scenario["domestic_tuition_revenue"] +
    scenario["scenario_international_tuition_revenue"] +
    scenario["operating_grant"] +
    scenario["special_purpose_grants"]
)

scenario["revenue_impact"] = (
    scenario["scenario_total_revenue"] -
    scenario["baseline_total_revenue"]
)

scenario["revenue_impact_pct"] = (
    scenario["revenue_impact"] /
    scenario["baseline_total_revenue"]
)

gold_international_scenario = scenario[
    [
        "scenario_name",
        "university",
        "university_profile",
        "year",
        "baseline_total_revenue",
        "scenario_total_revenue",
        "revenue_impact",
        "revenue_impact_pct",
        "international_enrolment",
        "scenario_international_enrolment",
        "international_tuition_dependency_ratio"
    ]
].copy()

gold_international_scenario = gold_international_scenario.round(4)

gold_international_scenario.to_csv(
    gold_path / "gold_international_enrolment_scenario.csv",
    index=False
)


# ============================================================
# GOLD TABLE 5: TUITION FREEZE SCENARIO
# ============================================================
# This scenario estimates the impact of domestic tuition remaining
# flat while inflation increases costs.
#
# It creates a simple inflation-adjusted pressure metric.
# ============================================================

tuition_freeze = latest_data.copy()

tuition_freeze["scenario_name"] = "domestic_tuition_freeze_inflation_pressure"

tuition_freeze["estimated_cost_pressure"] = (
    tuition_freeze["baseline_total_revenue"] if "baseline_total_revenue" in tuition_freeze.columns else
    (
        tuition_freeze["total_tuition_revenue"] +
        tuition_freeze["operating_grant"] +
        tuition_freeze["special_purpose_grants"]
    )
)

tuition_freeze["inflation_cost_pressure"] = (
    tuition_freeze["estimated_cost_pressure"] *
    tuition_freeze["inflation_rate"]
)

tuition_freeze["domestic_tuition_revenue_at_3pct_growth"] = (
    tuition_freeze["domestic_tuition_revenue"] * 1.03
)

tuition_freeze["foregone_domestic_tuition_revenue"] = (
    tuition_freeze["domestic_tuition_revenue_at_3pct_growth"] -
    tuition_freeze["domestic_tuition_revenue"]
)

gold_tuition_freeze_scenario = tuition_freeze[
    [
        "scenario_name",
        "university",
        "university_profile",
        "year",
        "domestic_tuition_revenue",
        "domestic_tuition_revenue_at_3pct_growth",
        "foregone_domestic_tuition_revenue",
        "inflation_rate",
        "inflation_cost_pressure"
    ]
].copy()

gold_tuition_freeze_scenario = gold_tuition_freeze_scenario.round(2)

gold_tuition_freeze_scenario.to_csv(
    gold_path / "gold_tuition_freeze_scenario.csv",
    index=False
)


# ============================================================
# 6. Print completion summary
# ============================================================

print("Gold layer created successfully.")
print(f"Gold files saved in: {gold_path}")

print("\nFiles created:")
print("- gold_sector_kpi_summary.csv")
print("- gold_university_kpi_summary.csv")
print("- gold_policy_risk_summary.csv")
print("- gold_international_enrolment_scenario.csv")
print("- gold_tuition_freeze_scenario.csv")

print("\nPreview: Sector KPI Summary")
print(gold_sector_kpis.head())

print("\nPreview: Policy Risk Summary")
print(gold_policy_risk.head())
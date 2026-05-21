import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# Silver Layer Transformation
# Project: Ontario University Policy Analytics Platform
#
# Purpose:
# This script takes the raw Bronze data files and transforms them
# into a clean, standardized, analytics-ready Silver dataset.
#
# Bronze layer:
#   Raw source-like data with duplicates, missing values, and
#   inconsistent naming.
#
# Silver layer:
#   Cleaned, standardized, joined, and validated data that can be
#   used for KPI reporting, forecasting, and policy analysis.
# ============================================================


# -----------------------------
# 1. Define project folders
# -----------------------------
base_path = Path("ontario_university_policy_analytics")

bronze_path = base_path / "data" / "bronze"
silver_path = base_path / "data" / "silver"

silver_path.mkdir(parents=True, exist_ok=True)


# -----------------------------
# 2. Load Bronze files
# -----------------------------
# These are the raw files created in the Bronze data generator.
enrolment = pd.read_csv(bronze_path / "bronze_enrolment.csv")
tuition = pd.read_csv(bronze_path / "bronze_tuition.csv")
grants = pd.read_csv(bronze_path / "bronze_operating_grants.csv")
macro = pd.read_csv(bronze_path / "bronze_policy_macro_factors.csv")


# -----------------------------
# 3. Standardize university names
# -----------------------------
# In the Bronze layer, we intentionally inserted an inconsistent
# university name: "Univ. of Toronto".
#
# In the Silver layer, we standardize it to the official name.
university_name_map = {
    "Univ. of Toronto": "University of Toronto",
    "University of Toronto": "University of Toronto"
}

enrolment["university"] = enrolment["university"].replace(university_name_map)
tuition["university"] = tuition["university"].replace(university_name_map)
grants["university"] = grants["university"].replace(university_name_map)


# -----------------------------
# 4. Remove duplicate records
# -----------------------------
# Bronze data may contain duplicate rows.
# We remove exact duplicates first.
enrolment = enrolment.drop_duplicates()
tuition = tuition.drop_duplicates()
grants = grants.drop_duplicates()
macro = macro.drop_duplicates()


# -----------------------------
# 5. Handle missing enrolment values
# -----------------------------
# The Bronze data intentionally contains a missing domestic enrolment value.
#
# Since enrolment is time-series data, interpolation is a reasonable
# cleaning method. It estimates a missing value using nearby years for
# the same university.
enrolment = enrolment.sort_values(["university", "year"])

enrolment["domestic_enrolment"] = (
    enrolment
    .groupby("university")["domestic_enrolment"]
    .transform(lambda x: x.interpolate(method="linear"))
)

# If any missing values remain at the beginning or end of a time series,
# fill them using forward-fill and backward-fill.
enrolment["domestic_enrolment"] = (
    enrolment
    .groupby("university")["domestic_enrolment"]
    .transform(lambda x: x.ffill().bfill())
)


# -----------------------------
# 6. Ensure numeric fields are numeric
# -----------------------------
# This protects the pipeline from raw data issues where numbers may be
# read as text.
numeric_cols_enrolment = [
    "domestic_enrolment",
    "international_enrolment",
    "graduate_share",
    "professional_program_share"
]

for col in numeric_cols_enrolment:
    enrolment[col] = pd.to_numeric(enrolment[col], errors="coerce")

numeric_cols_tuition = [
    "avg_domestic_tuition",
    "avg_international_tuition"
]

for col in numeric_cols_tuition:
    tuition[col] = pd.to_numeric(tuition[col], errors="coerce")

numeric_cols_grants = [
    "operating_grant",
    "special_purpose_grants"
]

for col in numeric_cols_grants:
    grants[col] = pd.to_numeric(grants[col], errors="coerce")


# -----------------------------
# 7. Merge enrolment and tuition data
# -----------------------------
# The first merge combines student counts with tuition rates.
silver = enrolment.merge(
    tuition,
    on=["university", "year"],
    how="left"
)


# -----------------------------
# 8. Merge operating grant data
# -----------------------------
# This adds operating grants and special purpose grants.
silver = silver.merge(
    grants,
    on=["university", "year"],
    how="left"
)


# -----------------------------
# 9. Merge macro and policy factors
# -----------------------------
# Macro data is annual, not university-specific.
# Therefore, we merge only on year.
silver = silver.merge(
    macro,
    on="year",
    how="left"
)


# -----------------------------
# 10. Create core enrolment KPIs
# -----------------------------
# These metrics support enrolment trend analysis.
silver["total_enrolment"] = (
    silver["domestic_enrolment"] + silver["international_enrolment"]
)

silver["international_share"] = (
    silver["international_enrolment"] / silver["total_enrolment"]
)

silver["domestic_share"] = (
    silver["domestic_enrolment"] / silver["total_enrolment"]
)


# -----------------------------
# 11. Create tuition revenue metrics
# -----------------------------
# These estimate tuition revenue by student group.
silver["domestic_tuition_revenue"] = (
    silver["domestic_enrolment"] * silver["avg_domestic_tuition"]
)

silver["international_tuition_revenue"] = (
    silver["international_enrolment"] * silver["avg_international_tuition"]
)

silver["total_tuition_revenue"] = (
    silver["domestic_tuition_revenue"] +
    silver["international_tuition_revenue"]
)


# -----------------------------
# 12. Create grant and funding metrics
# -----------------------------
# These metrics are useful for policy and funding analysis.
silver["total_grants"] = (
    silver["operating_grant"] + silver["special_purpose_grants"]
)

silver["funding_per_student"] = (
    silver["operating_grant"] / silver["total_enrolment"]
)

silver["grant_dependency_ratio"] = (
    silver["operating_grant"] /
    (silver["operating_grant"] + silver["total_tuition_revenue"])
)

silver["international_tuition_dependency_ratio"] = (
    silver["international_tuition_revenue"] /
    silver["total_tuition_revenue"]
)


# -----------------------------
# 13. Create year-over-year trend metrics
# -----------------------------
# These metrics support trend analysis and executive briefing.
silver = silver.sort_values(["university", "year"])

silver["total_enrolment_yoy_growth"] = (
    silver
    .groupby("university")["total_enrolment"]
    .pct_change()
)

silver["tuition_revenue_yoy_growth"] = (
    silver
    .groupby("university")["total_tuition_revenue"]
    .pct_change()
)

silver["operating_grant_yoy_growth"] = (
    silver
    .groupby("university")["operating_grant"]
    .pct_change()
)


# -----------------------------
# 14. Create simple policy risk flags
# -----------------------------
# These flags are useful for policy scenario analysis.
#
# Example:
# A university with high international share may be more exposed to
# policy changes affecting international enrolment.
silver["high_international_exposure_flag"] = np.where(
    silver["international_share"] >= 0.30,
    1,
    0
)

silver["high_grant_dependency_flag"] = np.where(
    silver["grant_dependency_ratio"] >= 0.50,
    1,
    0
)


# -----------------------------
# 15. Round selected numeric fields
# -----------------------------
# Rounding improves readability for reporting and dashboards.
ratio_cols = [
    "international_share",
    "domestic_share",
    "grant_dependency_ratio",
    "international_tuition_dependency_ratio",
    "total_enrolment_yoy_growth",
    "tuition_revenue_yoy_growth",
    "operating_grant_yoy_growth"
]

for col in ratio_cols:
    silver[col] = silver[col].round(4)

money_cols = [
    "domestic_tuition_revenue",
    "international_tuition_revenue",
    "total_tuition_revenue",
    "total_grants",
    "funding_per_student"
]

for col in money_cols:
    silver[col] = silver[col].round(2)


# -----------------------------
# 16. Basic validation checks
# -----------------------------
# These checks help confirm that the Silver layer is reliable.
print("Silver layer validation checks:")
print("--------------------------------")
print("Rows:", len(silver))
print("Missing values by column:")
print(silver.isna().sum())

print("\nDuplicate university-year records:")
print(silver.duplicated(subset=["university", "year"]).sum())


# -----------------------------
# 17. Save Silver dataset
# -----------------------------
# This file becomes the trusted analytics-ready dataset.
silver.to_csv(
    silver_path / "silver_university_financials.csv",
    index=False
)

print("\nSilver dataset created successfully.")
print(f"File saved to: {silver_path / 'silver_university_financials.csv'}")

print("\nPreview of Silver dataset:")
print(silver.head())
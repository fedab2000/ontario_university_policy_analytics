import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# Synthetic Data Generator
# Project: Ontario University Policy Analytics Platform
#
# Purpose:
# This script creates synthetic data for a policy analytics project
# focused on Ontario universities. The data is designed to support
# analysis of enrolment trends, tuition revenue, operating grants,
# and policy scenario modelling.
#
# The generated files represent the Bronze layer of a Medallion
# Architecture:
#   Bronze = raw / source-like data
#   Silver = cleaned and standardized data
#   Gold   = curated business-ready analytics data
# ============================================================


# -----------------------------
# 1. Set random seed
# -----------------------------
# A random seed makes the synthetic data reproducible.
# This means every time you run the script, you will get the same
# synthetic dataset unless you change the seed value.
np.random.seed(42)


# -----------------------------
# 2. Create project folders
# -----------------------------
# This creates a project folder structure that mirrors a real
# data engineering / analytics project.
#
# data/bronze = raw source-like files
# data/silver = cleaned and standardized files
# data/gold   = final KPI and analytics-ready files
base_path = Path("ontario_university_policy_analytics")

bronze_path = base_path / "data" / "bronze"
silver_path = base_path / "data" / "silver"
gold_path = base_path / "data" / "gold"

# Create the folders if they do not already exist.
# parents=True allows Python to create intermediate folders.
# exist_ok=True prevents an error if the folders already exist.
for path in [bronze_path, silver_path, gold_path]:
    path.mkdir(parents=True, exist_ok=True)


# -----------------------------
# 3. Define synthetic universities
# -----------------------------
# These are Ontario universities used for the synthetic dataset.
# The names are realistic, but the numbers generated below are synthetic.
universities = [
    "University of Toronto",
    "University of Waterloo",
    "McMaster University",
    "Western University",
    "Queen's University",
    "York University",
    "University of Ottawa",
    "Carleton University",
    "Toronto Metropolitan University",
    "Brock University",
    "Lakehead University",
    "Laurentian University"
]


# -----------------------------
# 4. Assign each university a profile
# -----------------------------
# The profile controls the size and behaviour of the synthetic data.
#
# For example:
# - large research universities have higher enrolment and grants
# - smaller regional universities have lower enrolment and grants
# - northern regional universities may be smaller but strategically important
#
# This creates more realistic variation across institutions.
university_profiles = {
    "University of Toronto": "large_research",
    "University of Waterloo": "large_research",
    "McMaster University": "large_research",
    "Western University": "large_research",
    "Queen's University": "mid_research",
    "York University": "large_comprehensive",
    "University of Ottawa": "large_comprehensive",
    "Carleton University": "mid_comprehensive",
    "Toronto Metropolitan University": "mid_comprehensive",
    "Brock University": "smaller_regional",
    "Lakehead University": "northern_regional",
    "Laurentian University": "northern_regional"
}


# -----------------------------
# 5. Define the analysis years
# -----------------------------
# The dataset covers multiple years so that we can analyze trends
# and later build forecasting or scenario models.
years = list(range(2016, 2027))


# ============================================================
# BRONZE FILE 1: ENROLMENT DATA
# ============================================================
# This table simulates annual domestic and international enrolment
# by university.
#
# It also includes:
# - graduate_share
# - professional_program_share
#
# These variables can later support analysis of revenue dependency,
# enrolment mix, and policy exposure.
# ============================================================

enrolment_rows = []

for uni in universities:
    profile = university_profiles[uni]

    # Assign baseline domestic and international enrolment based on
    # the university profile.
    if profile == "large_research":
        base_domestic = np.random.randint(28000, 65000)
        base_international = np.random.randint(7000, 22000)

    elif profile == "large_comprehensive":
        base_domestic = np.random.randint(25000, 55000)
        base_international = np.random.randint(5000, 16000)

    elif profile == "mid_research":
        base_domestic = np.random.randint(16000, 32000)
        base_international = np.random.randint(3000, 9000)

    elif profile == "mid_comprehensive":
        base_domestic = np.random.randint(14000, 30000)
        base_international = np.random.randint(2500, 8000)

    else:
        # Smaller and northern regional universities
        base_domestic = np.random.randint(4000, 14000)
        base_international = np.random.randint(500, 3000)

    for i, year in enumerate(years):

        # Domestic enrolment grows slowly and relatively steadily.
        domestic_growth = np.random.normal(0.008, 0.018)

        # International enrolment grows faster but with more volatility.
        international_growth = np.random.normal(0.045, 0.04)

        # Simulated policy shock:
        # Starting in 2024, international enrolment growth is reduced.
        # This mirrors a scenario where policy changes or federal caps
        # put pressure on international student growth.
        if year >= 2024:
            international_growth -= np.random.uniform(0.04, 0.09)

        # Apply compounded growth over time.
        domestic = int(base_domestic * ((1 + domestic_growth) ** i))
        international = int(base_international * ((1 + international_growth) ** i))

        enrolment_rows.append({
            "university": uni,
            "year": year,
            "university_profile": profile,
            "domestic_enrolment": max(domestic, 1000),
            "international_enrolment": max(international, 100),
            "graduate_share": round(np.random.uniform(0.12, 0.32), 3),
            "professional_program_share": round(np.random.uniform(0.04, 0.18), 3)
        })

bronze_enrolment = pd.DataFrame(enrolment_rows)


# -----------------------------
# Add intentional Bronze-layer messiness
# -----------------------------
# Real raw data is rarely perfect. To make this project more realistic,
# we intentionally introduce:
# - inconsistent naming
# - missing values
# - duplicate records
#
# These issues can later be fixed in the Silver layer.
bronze_enrolment.loc[3, "university"] = "Univ. of Toronto"
bronze_enrolment.loc[17, "domestic_enrolment"] = np.nan

bronze_enrolment = pd.concat(
    [bronze_enrolment, bronze_enrolment.sample(3, random_state=42)],
    ignore_index=True
)

# Save enrolment data to the Bronze folder.
bronze_enrolment.to_csv(bronze_path / "bronze_enrolment.csv", index=False)


# ============================================================
# BRONZE FILE 2: TUITION DATA
# ============================================================
# This table simulates average domestic and international tuition
# by university and year.
#
# It supports later analysis of:
# - tuition revenue
# - tuition dependency
# - domestic vs international revenue mix
# - policy effects of tuition freezes
# ============================================================

tuition_rows = []

for uni in universities:
    for year in years:

        # Generate base tuition values.
        domestic_base = np.random.randint(6800, 9500)
        international_base = np.random.randint(31000, 61000)

        # Simulated tuition policy:
        # Domestic tuition is assumed to be frozen after 2019.
        if year >= 2019:
            domestic_growth_factor = 1.00
        else:
            domestic_growth_factor = 1 + np.random.normal(0.02, 0.01)

        # International tuition continues to grow.
        international_growth_factor = 1 + np.random.normal(0.04, 0.015)

        tuition_rows.append({
            "university": uni,
            "year": year,
            "avg_domestic_tuition": round(domestic_base * domestic_growth_factor, 2),
            "avg_international_tuition": round(international_base * international_growth_factor, 2)
        })

bronze_tuition = pd.DataFrame(tuition_rows)

# Save tuition data to the Bronze folder.
bronze_tuition.to_csv(bronze_path / "bronze_tuition.csv", index=False)


# ============================================================
# BRONZE FILE 3: OPERATING GRANT DATA
# ============================================================
# This table simulates provincial operating grants and special
# purpose grants by university and year.
#
# This is highly relevant to the COU-style policy analytics use case,
# because operating grants are a major policy and financial planning area.
# ============================================================

grant_rows = []

for uni in universities:
    profile = university_profiles[uni]

    # Larger universities receive larger base operating grants.
    if "large" in profile:
        base_grant = np.random.randint(450_000_000, 1_200_000_000)

    elif "mid" in profile:
        base_grant = np.random.randint(220_000_000, 520_000_000)

    else:
        base_grant = np.random.randint(80_000_000, 240_000_000)

    for i, year in enumerate(years):

        # Normal annual grant growth.
        grant_growth = np.random.normal(0.012, 0.018)

        # Simulated restraint period:
        # During 2020-2022, growth is reduced to represent fiscal pressure.
        if year in [2020, 2021, 2022]:
            grant_growth -= np.random.uniform(0.005, 0.02)

        operating_grant = int(base_grant * ((1 + grant_growth) ** i))

        grant_rows.append({
            "university": uni,
            "year": year,
            "operating_grant": operating_grant,

            # Special purpose grants are a smaller share of operating grants.
            "special_purpose_grants": int(
                operating_grant * np.random.uniform(0.03, 0.11)
            )
        })

bronze_grants = pd.DataFrame(grant_rows)

# Save grant data to the Bronze folder.
bronze_grants.to_csv(bronze_path / "bronze_operating_grants.csv", index=False)


# ============================================================
# BRONZE FILE 4: POLICY AND MACRO FACTORS
# ============================================================
# This table simulates annual external factors that can affect
# university finances and planning.
#
# Examples:
# - inflation
# - provincial budget growth
# - tuition policy
# - international enrolment policy pressure
#
# This can later be joined to university-level data for scenario analysis.
# ============================================================

macro_rows = []

for year in years:
    macro_rows.append({
        "year": year,

        # Synthetic annual inflation rate.
        "inflation_rate": round(np.random.uniform(0.012, 0.068), 3),

        # Synthetic provincial budget growth.
        "provincial_budget_growth": round(np.random.uniform(-0.015, 0.045), 3),

        # Domestic tuition policy environment.
        "tuition_policy": "tuition_freeze" if year >= 2019 else "market_growth",

        # Indicator for international enrolment policy pressure.
        "international_policy_pressure": 1 if year >= 2024 else 0
    })

bronze_macro = pd.DataFrame(macro_rows)

# Save macro/policy factor data to the Bronze folder.
bronze_macro.to_csv(bronze_path / "bronze_policy_macro_factors.csv", index=False)


# ============================================================
# Final confirmation output
# ============================================================
# Print a confirmation message and preview the enrolment data.
print("Synthetic Bronze data created successfully.")
print(f"Files saved in: {bronze_path}")

print("\nPreview of bronze_enrolment:")
print(bronze_enrolment.head())
# Ontario University Policy Analytics Platform

## Overview

The Ontario University Policy Analytics Platform is a synthetic higher education analytics project designed to simulate how Ontario universities and sector organizations can use data to support strategic planning, policy analysis, and executive decision-making.

The project demonstrates how a Medallion Architecture (Bronze → Silver → Gold) can be used to transform raw institutional data into trusted analytics datasets and executive-ready policy insights.

The platform focuses on key higher education policy domains including:

- Enrolment trends
- Tuition revenue analysis
- Operating grant analysis
- International student dependency
- Policy risk assessment
- Financial scenario modelling

---

# Business Problem

Ontario universities face increasing financial and policy pressures related to:

- fluctuations in international enrolment
- tuition policy constraints
- operating grant dependency
- inflationary pressures
- long-term financial sustainability

Decision-makers require trusted, standardized, and analytics-ready data to support:

- policy development
- funding analysis
- executive reporting
- strategic planning
- scenario modelling

This project simulates a centralized analytics platform capable of supporting those objectives.

---

# Project Objectives

The objectives of this project are to:

- Design a Medallion Architecture analytics platform
- Simulate policy and financial analytics workflows
- Standardize and govern university data
- Create trusted analytics datasets
- Develop executive-ready KPI summaries
- Support quantitative policy analysis
- Model financial and enrolment scenarios

---

# Architecture

## Bronze Layer — Raw Source Data

The Bronze layer simulates raw institutional data sources.

Characteristics:
- inconsistent naming
- duplicate records
- missing values
- separate operational datasets

Bronze datasets include:
- enrolment data
- tuition data
- operating grant data
- macroeconomic and policy factors

### Bronze Files

```text
data/bronze/
│
├── bronze_enrolment.csv
├── bronze_tuition.csv
├── bronze_operating_grants.csv
└── bronze_policy_macro_factors.csv

Silver Layer — Trusted Analytics Layer

The Silver layer standardizes and cleans the Bronze data.

Key transformations include:

university name standardization
duplicate removal
missing value handling
KPI derivation
financial calculations
policy indicator creation
dataset integration

The Silver layer acts as the trusted analytics foundation for reporting and modelling.

Silver Files
data/silver/
│
└── silver_university_financials.csv

Example Silver KPIs
Total enrolment
International student share
Tuition revenue
Funding per student
Grant dependency ratio
Year-over-year growth metrics
Policy exposure indicators

Gold Layer — Executive & Policy Analytics

The Gold layer produces business-ready analytics outputs for executive reporting and policy analysis.

Gold outputs include:

sector KPI summaries
university KPI comparisons
policy risk scoring
international enrolment impact scenarios
tuition freeze scenario analysis
Gold Files
data/gold/
│
├── gold_sector_kpi_summary.csv
├── gold_university_kpi_summary.csv
├── gold_policy_risk_summary.csv
├── gold_international_enrolment_scenario.csv
└── gold_tuition_freeze_scenario.csv

Repository Structure
ontario-university-policy-analytics/
│
├── data/
│   ├── bronze/
│   │   ├── bronze_enrolment.csv
│   │   ├── bronze_tuition.csv
│   │   ├── bronze_operating_grants.csv
│   │   └── bronze_policy_macro_factors.csv
│   │
│   ├── silver/
│   │   └── silver_university_financials.csv
│   │
│   └── gold/
│       ├── gold_sector_kpi_summary.csv
│       ├── gold_university_kpi_summary.csv
│       ├── gold_policy_risk_summary.csv
│       ├── gold_international_enrolment_scenario.csv
│       └── gold_tuition_freeze_scenario.csv
│
├
│── bronzeLayer.py
│── silverLayer.py
│── goldLayer.py
│
├── visuals/
│
├── README.md
├── requirements.txt
└── .gitignore

Key Features
Enrolment Analytics
Domestic and international enrolment analysis
Enrolment trend tracking
International enrolment exposure analysis
Graduate and professional program analysis

Financial Analytics
Tuition revenue modelling
Operating grant analysis
Funding-per-student metrics
Grant dependency analysis
Inflation-adjusted financial analysis

Policy Analytics
Policy risk scoring
Scenario modelling
Inflation impact analysis
Tuition freeze modelling
International enrolment decline simulations

Data Governance
Standardized university naming
Trusted KPI definitions
Medallion Architecture implementation
Single-source-of-truth analytics design
Analytics-ready data modelling

Scenario Modelling
The project includes several policy and financial scenarios.

International Enrolment Decline Scenario

Models the impact of a 10% decline in international enrolment on university revenue.

Metrics include:

revenue impact
percentage revenue decline
tuition dependency exposure
university-level financial pressure

Tuition Freeze Scenario

Estimates the financial pressure created by tuition freezes under inflationary conditions.

Metrics include:

foregone tuition revenue
inflation-adjusted cost pressure
estimated financial gap

Example Executive KPIs

The platform produces analytics-ready KPIs including:

Total enrolment
Domestic vs international enrolment mix
Tuition revenue
Operating grant allocation
Funding per student
Grant dependency ratio
International tuition dependency
Year-over-year enrolment growth
Revenue growth trends

Technology Stack
Python
Pandas
NumPy
Medallion Architecture
Quantitative Policy Analysis
Financial Modelling
Data Governance Concepts

How to Run the Project
Step 1 — Generate Bronze Data

Run:
python scripts/01_bronze_data_generator.py
This creates the synthetic Bronze datasets.

Step 2 — Build the Silver Layer

Run:
python scripts/02_silver_transformation.py
This cleans and standardizes the Bronze data and generates the trusted Silver dataset.

Step 3 — Build the Gold Layer

Run:
python scripts/03_gold_layer.py
This creates executive-ready KPI and policy analytics outputs.

Example Use Cases

This platform can support:

executive reporting
policy briefing notes
strategic planning
funding analysis
enrolment forecasting
scenario modelling
institutional benchmarking
Potential Future Enhancements

Future enhancements could include:

Power BI dashboards
Streamlit web application
Machine learning forecasting
Predictive enrolment modelling
Cloud deployment using Azure or Databricks
Interactive policy simulation tools
Executive scorecards
Automated briefing note generation
Key Learning Outcomes

This project demonstrates:

Medallion Architecture implementation
Data engineering workflows
Data governance concepts
Quantitative policy analytics
Executive KPI modelling
Financial scenario analysis
Strategic analytics design
Author

Feda Bashbishi
MBA, M.Sc. Eng., MDSAI
University of Waterloo

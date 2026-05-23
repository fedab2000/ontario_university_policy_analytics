
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# Ontario University Policy Analytics Platform
# Streamlit Executive Dashboard
#
# Author: Feda Bashbishi fbashbis@uwaterloo.ca
#
# Purpose:
# Interactive dashboard for analyzing Ontario university policy,
# enrolment, tuition, funding, and scenario risk using a
# Medallion Architecture data project.
# ============================================================

st.set_page_config(
    page_title="Ontario University Policy Analytics",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# Helper functions
# -----------------------------
@st.cache_data
def load_csv(file_name: str) -> pd.DataFrame:
    """
    Load CSV files from common project locations.
    This makes the app work both locally and on Streamlit Cloud.
    """
    possible_paths = [
        Path(file_name),
        Path("data") / "gold" / file_name,
        Path("data") / "silver" / file_name,
        Path("ontario_university_policy_analytics") / "data" / "gold" / file_name,
        Path("ontario_university_policy_analytics") / "data" / "silver" / file_name,
    ]

    for path in possible_paths:
        if path.exists():
            return pd.read_csv(path)

    st.error(f"Could not find {file_name}. Please check your GitHub folder structure.")
    st.stop()


def format_currency(value):
    return f"${value:,.0f}"


def format_number(value):
    return f"{value:,.0f}"


def format_percent(value):
    return f"{value:.1%}"


# -----------------------------
# Load data
# -----------------------------
sector_kpi = load_csv("gold_sector_kpi_summary.csv")
policy_risk = load_csv("gold_policy_risk_summary.csv")
international_scenario = load_csv("gold_international_enrolment_scenario.csv")
tuition_freeze = load_csv("gold_tuition_freeze_scenario.csv")
silver = load_csv("silver_university_financials.csv")

# Ensure year is numeric
for df in [sector_kpi, policy_risk, international_scenario, tuition_freeze, silver]:
    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Dashboard Controls")

available_years = sorted(silver["year"].dropna().unique())
selected_year = st.sidebar.selectbox(
    "Select year",
    available_years,
    index=len(available_years) - 1
)

available_profiles = sorted(silver["university_profile"].dropna().unique())
selected_profiles = st.sidebar.multiselect(
    "Select university profile",
    available_profiles,
    default=available_profiles
)

available_universities = sorted(silver["university"].dropna().unique())
selected_universities = st.sidebar.multiselect(
    "Select universities",
    available_universities,
    default=available_universities
)

st.sidebar.markdown("---")
st.sidebar.caption("Tip: Use the filters to compare institutional exposure, revenue dependency, and scenario impacts.")

# Filtered data
filtered_silver = silver[
    (silver["year"] == selected_year)
    & (silver["university_profile"].isin(selected_profiles))
    & (silver["university"].isin(selected_universities))
].copy()

filtered_risk = policy_risk[
    (policy_risk["year"] == selected_year)
    & (policy_risk["university_profile"].isin(selected_profiles))
    & (policy_risk["university"].isin(selected_universities))
].copy()

filtered_intl_scenario = international_scenario[
    (international_scenario["year"] == selected_year)
    & (international_scenario["university_profile"].isin(selected_profiles))
    & (international_scenario["university"].isin(selected_universities))
].copy()

filtered_tuition_freeze = tuition_freeze[
    (tuition_freeze["year"] == selected_year)
    & (tuition_freeze["university_profile"].isin(selected_profiles))
    & (tuition_freeze["university"].isin(selected_universities))
].copy()

# -----------------------------
# Header
# -----------------------------
st.title("🎓 Ontario University Policy Analytics Platform")
st.markdown(
    """
    This executive dashboard analyzes Ontario university enrolment, tuition revenue,
    operating grants, funding dependency, and policy scenario risks using a
    Bronze → Silver → Gold analytics architecture.
    """
)

st.info(
    "Note: This project uses synthetic data for portfolio and demonstration purposes. "
    "The structure is designed to mirror a real policy analytics use case."
)

# -----------------------------
# Executive KPI cards
# -----------------------------
latest_sector = sector_kpi[sector_kpi["year"] == selected_year]

if latest_sector.empty:
    st.warning("No sector KPI data is available for the selected year.")
else:
    latest_sector = latest_sector.iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Enrolment",
            format_number(latest_sector["total_enrolment"])
        )

    with col2:
        st.metric(
            "International Share",
            format_percent(latest_sector["sector_international_share"])
        )

    with col3:
        st.metric(
            "Total Tuition Revenue",
            format_currency(latest_sector["total_tuition_revenue"])
        )

    with col4:
        st.metric(
            "Grant Dependency",
            format_percent(latest_sector["sector_grant_dependency_ratio"])
        )

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Executive Overview",
        "University Comparison",
        "Policy Risk",
        "Scenario Analysis",
        "Data Explorer"
    ]
)

# ============================================================
# TAB 1: Executive Overview
# ============================================================
with tab1:
    st.subheader("Sector Trends")

    trend_col1, trend_col2 = st.columns(2)

    with trend_col1:
        fig = px.line(
            sector_kpi,
            x="year",
            y=["total_domestic_enrolment", "total_international_enrolment"],
            markers=True,
            title="Domestic vs International Enrolment Trend",
            labels={
                "value": "Students",
                "year": "Year",
                "variable": "Enrolment Type"
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    with trend_col2:
        fig = px.line(
            sector_kpi,
            x="year",
            y=["total_tuition_revenue", "total_operating_grant"],
            markers=True,
            title="Tuition Revenue vs Operating Grants",
            labels={
                "value": "Dollars",
                "year": "Year",
                "variable": "Funding Source"
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    trend_col3, trend_col4 = st.columns(2)

    with trend_col3:
        fig = px.line(
            sector_kpi,
            x="year",
            y="sector_international_share",
            markers=True,
            title="Sector International Enrolment Share",
            labels={
                "sector_international_share": "International Share",
                "year": "Year"
            }
        )
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

    with trend_col4:
        fig = px.line(
            sector_kpi,
            x="year",
            y="sector_funding_per_student",
            markers=True,
            title="Sector Operating Grant Funding Per Student",
            labels={
                "sector_funding_per_student": "Funding Per Student",
                "year": "Year"
            }
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 2: University Comparison
# ============================================================
with tab2:
    st.subheader(f"University Comparison — {selected_year}")

    if filtered_silver.empty:
        st.warning("No data available for the selected filters.")
    else:
        metric_option = st.selectbox(
            "Choose comparison metric",
            [
                "total_enrolment",
                "international_share",
                "total_tuition_revenue",
                "operating_grant",
                "funding_per_student",
                "grant_dependency_ratio",
                "international_tuition_dependency_ratio"
            ],
            index=0
        )

        comparison = filtered_silver.sort_values(metric_option, ascending=False)

        fig = px.bar(
            comparison,
            x="university",
            y=metric_option,
            color="university_profile",
            title=f"{metric_option.replace('_', ' ').title()} by University",
            labels={
                "university": "University",
                metric_option: metric_option.replace("_", " ").title(),
                "university_profile": "Profile"
            }
        )
        fig.update_layout(xaxis_tickangle=-45)
        if "share" in metric_option or "ratio" in metric_option:
            fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Filtered University KPI Table")
        display_cols = [
            "university",
            "university_profile",
            "total_enrolment",
            "international_share",
            "total_tuition_revenue",
            "operating_grant",
            "funding_per_student",
            "grant_dependency_ratio",
            "international_tuition_dependency_ratio"
        ]
        st.dataframe(
            comparison[display_cols],
            use_container_width=True,
            hide_index=True
        )

# ============================================================
# TAB 3: Policy Risk
# ============================================================
with tab3:
    st.subheader("Policy Risk Summary")

    st.markdown(
        """
        The policy risk score combines international enrolment exposure,
        international tuition dependency, and operating grant dependency into
        an interpretable executive-facing indicator.
        """
    )

    if filtered_risk.empty:
        st.warning("No policy risk data available for the selected filters.")
    else:
        risk_col1, risk_col2 = st.columns([2, 1])

        with risk_col1:
            fig = px.bar(
                filtered_risk.sort_values("policy_risk_score", ascending=True),
                x="policy_risk_score",
                y="university",
                color="policy_risk_level",
                orientation="h",
                title="Policy Risk Score by University",
                labels={
                    "policy_risk_score": "Policy Risk Score",
                    "university": "University",
                    "policy_risk_level": "Risk Level"
                }
            )
            st.plotly_chart(fig, use_container_width=True)

        with risk_col2:
            risk_counts = (
                filtered_risk["policy_risk_level"]
                .value_counts()
                .rename_axis("policy_risk_level")
                .reset_index(name="count")
            )
            fig = px.pie(
                risk_counts,
                values="count",
                names="policy_risk_level",
                title="Risk Level Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Highest Risk Institutions")
        risk_table = filtered_risk.sort_values("policy_risk_score", ascending=False)
        st.dataframe(risk_table, use_container_width=True, hide_index=True)

# ============================================================
# TAB 4: Scenario Analysis
# ============================================================
with tab4:
    st.subheader("Scenario Analysis")

    scenario_choice = st.radio(
        "Select scenario",
        [
            "10% International Enrolment Decline",
            "Domestic Tuition Freeze + Inflation Pressure"
        ],
        horizontal=True
    )

    if scenario_choice == "10% International Enrolment Decline":
        st.markdown(
            """
            This scenario estimates the financial impact of a 10% decline in
            international enrolment for the selected year.
            """
        )

        if filtered_intl_scenario.empty:
            st.warning("No international enrolment scenario data available for the selected filters.")
        else:
            total_impact = filtered_intl_scenario["revenue_impact"].sum()
            avg_impact_pct = filtered_intl_scenario["revenue_impact_pct"].mean()

            col1, col2 = st.columns(2)
            col1.metric("Total Revenue Impact", format_currency(total_impact))
            col2.metric("Average Revenue Impact %", format_percent(avg_impact_pct))

            fig = px.bar(
                filtered_intl_scenario.sort_values("revenue_impact"),
                x="revenue_impact",
                y="university",
                color="university_profile",
                orientation="h",
                title="Revenue Impact from 10% International Enrolment Decline",
                labels={
                    "revenue_impact": "Revenue Impact",
                    "university": "University",
                    "university_profile": "Profile"
                }
            )
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(
                filtered_intl_scenario.sort_values("revenue_impact"),
                use_container_width=True,
                hide_index=True
            )

    else:
        st.markdown(
            """
            This scenario estimates foregone domestic tuition revenue under a
            tuition freeze, alongside inflation-driven cost pressure.
            """
        )

        if filtered_tuition_freeze.empty:
            st.warning("No tuition freeze scenario data available for the selected filters.")
        else:
            total_foregone = filtered_tuition_freeze["foregone_domestic_tuition_revenue"].sum()
            total_inflation_pressure = filtered_tuition_freeze["inflation_cost_pressure"].sum()

            col1, col2 = st.columns(2)
            col1.metric("Foregone Domestic Tuition Revenue", format_currency(total_foregone))
            col2.metric("Inflation Cost Pressure", format_currency(total_inflation_pressure))

            fig = px.bar(
                filtered_tuition_freeze.sort_values("inflation_cost_pressure", ascending=False),
                x="university",
                y=["foregone_domestic_tuition_revenue", "inflation_cost_pressure"],
                title="Tuition Freeze and Inflation Pressure by University",
                labels={
                    "value": "Dollars",
                    "university": "University",
                    "variable": "Metric"
                }
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(
                filtered_tuition_freeze.sort_values("inflation_cost_pressure", ascending=False),
                use_container_width=True,
                hide_index=True
            )

# ============================================================
# TAB 5: Data Explorer
# ============================================================
with tab5:
    st.subheader("Data Explorer")

    dataset_choice = st.selectbox(
        "Choose dataset",
        [
            "Silver University Financials",
            "Gold Sector KPI Summary",
            "Gold Policy Risk Summary",
            "Gold International Enrolment Scenario",
            "Gold Tuition Freeze Scenario"
        ]
    )

    dataset_map = {
        "Silver University Financials": silver,
        "Gold Sector KPI Summary": sector_kpi,
        "Gold Policy Risk Summary": policy_risk,
        "Gold International Enrolment Scenario": international_scenario,
        "Gold Tuition Freeze Scenario": tuition_freeze
    }

    selected_df = dataset_map[dataset_choice]

    st.write(f"Rows: {selected_df.shape[0]:,} | Columns: {selected_df.shape[1]:,}")
    st.dataframe(selected_df, use_container_width=True, hide_index=True)

    csv = selected_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download selected dataset as CSV",
        data=csv,
        file_name=f"{dataset_choice.lower().replace(' ', '_')}.csv",
        mime="text/csv"
    )

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("Author: Feda Bashbishi fbashbis@uwaterloo.ca")

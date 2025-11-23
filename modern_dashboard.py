import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

st.set_page_config(
    page_title="Inclusive Digital Healthcare Dashboard 🇪🇺",
    layout="wide",
    page_icon="🩺"
)

# ---------------------------------------
# CACHE DATABASE & DATA LOADING
# ---------------------------------------

@st.cache_resource
def get_engine():
    return create_engine("sqlite:///access_project.db")


@st.cache_data
def load_profiles():
    df = pd.read_csv("patient_profiles_europe.csv")
    df["patient_id"] = df["patient_id"].astype(int)
    return df


@st.cache_data
def load_feedback_csv():
    df = pd.read_csv("feedback_flattened.csv")
    if "_id" in df.columns:
        df = df.drop(columns=["_id"])
    df["patient_id"] = df["patient_id"].astype(int)
    return df


@st.cache_data
def merge_data():
    df_profiles = load_profiles()
    df_feedback = load_feedback_csv()

    merged = pd.merge(
        df_profiles, df_feedback,
        on="patient_id", suffixes=("_profile", "_feedback")
    )

    if "satisfaction_score" in merged.columns:
        merged["satisfaction_score"] = merged["satisfaction_score"].fillna(
            merged["satisfaction_score"].mean()
        )

    # Save to SQL
    engine = get_engine()
    merged.to_sql("merged_access_data", engine, if_exists="replace", index=False)

    return merged


# ---------------------------------------
# LOAD MERGED DATA
# ---------------------------------------
merged_df = merge_data()


# ---------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------
st.title("Inclusive Digital Healthcare in Europe")
st.caption("Analytical Visualization of Accessibility Challenges")

st.sidebar.header("Filter Data")

country_list = ['All'] + sorted(merged_df['country_profile'].unique().tolist())
country = st.sidebar.selectbox("Country", country_list)

if country != "All":
    data = merged_df[merged_df["country_profile"] == country]
else:
    data = merged_df


# ---------------------------------------
# KPIs
# ---------------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Patients", f"{data['patient_id'].nunique():,}")
col2.metric("Countries", f"{data['country_profile'].nunique()}")
col3.metric("Accessibility Types", f"{data['accessibility_type'].nunique()}")
col4.metric("Avg. Satisfaction", f"{data['satisfaction_score'].mean():.2f} / 5")

st.write("---")


# ---------------------------------------
# PLOTS
# ---------------------------------------

c1, c2 = st.columns([1.2, 1])

# Plot 1 - Country Distribution
with c1:
    st.subheader("Top 10 Patient Populations by Country")
    fig, ax = plt.subplots(figsize=(8, 4))
    colors = sns.color_palette("crest", as_cmap=True)
    (data["country_profile"].value_counts().head(10).sort_values()).plot.barh(
        ax=ax, color=colors(range(10))
    )
    ax.set_xlabel("Patient Count")
    ax.set_ylabel("Country")
    st.pyplot(fig)

# Plot 2 - Satisfaction by Accessibility Type
with c2:
    st.subheader("Satisfaction Score by Accessibility Type")
    fig2, ax2 = plt.subplots(figsize=(5, 4))
    sns.barplot(
        x=data["accessibility_type"],
        y=data["satisfaction_score"],
        ax=ax2,
        palette="mako",
        errorbar=None
    )
    ax2.set_ylabel("Avg. Satisfaction")
    ax2.set_xlabel("Accessibility Type")
    plt.ylim(1, 5)
    st.pyplot(fig2)


# ---------------------------------------
# Row 2 - Demographics
# ---------------------------------------
c3, c4 = st.columns(2)

with c3:
    st.subheader("Gender Balance")
    gender_counts = data["gender"].value_counts()
    fig3, ax3 = plt.subplots(figsize=(3, 3))
    ax3.pie(
        gender_counts,
        labels=gender_counts.index,
        autopct="%1.1f%%",
        colors=sns.color_palette("pastel"),
        startangle=150,
        wedgeprops=dict(width=0.5)
    )
    st.pyplot(fig3)

with c4:
    st.subheader("Feedback Issue Types")
    issue_counts = data["issue_type"].value_counts().head(6)
    fig4, ax4 = plt.subplots(figsize=(5, 3))
    sns.barplot(
        y=issue_counts.index,
        x=issue_counts.values,
        ax=ax4,
        hue=issue_counts.index,
        dodge=False,
        palette="flare"
    )
    ax4.legend([], [], frameon=False)
    ax4.set_xlabel("Count")
    ax4.set_ylabel("Issue Type")
    st.pyplot(fig4)


# ---------------------------------------
# Row 3 - Age & Device
# ---------------------------------------
d1, d2 = st.columns(2)

with d1:
    st.subheader("Age Distribution")
    fig5, ax5 = plt.subplots(figsize=(6, 2.5))
    sns.histplot(data["age"], bins=20, color="#3984e8")
    ax5.set_xlabel("Age")
    st.pyplot(fig5)

with d2:
    st.subheader("Device Type Usage")
    fig6, ax6 = plt.subplots(figsize=(3, 2.5))
    sns.countplot(x="device_type", data=data, palette="viridis", ax=ax6)
    ax6.set_xlabel("Device")
    ax6.set_ylabel("Patients")
    st.pyplot(fig6)


# ---------------------------------------
# DATA TABLE
# ---------------------------------------
with st.expander("🔎 Preview Cleaned Dataset (First 100 Rows)"):
    st.dataframe(data.head(100))


# ---------------------------------------
# FOOTER
# ---------------------------------------
st.write("---")
st.markdown("""
<small>
Dashboard by <b>Keerthika Santhanakrishnan</b> | <b>Ragul Thangavel</b><br>
Project: <b>Enabling Inclusive Digital Healthcare Through Analytical Visualization of Accessibility Challenges</b>
</small>
""", unsafe_allow_html=True)

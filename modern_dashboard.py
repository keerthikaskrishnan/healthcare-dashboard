import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

import pandas as pd
from sqlalchemy import create_engine
from pymongo import MongoClient

# Read patient profiles from SQL
engine = create_engine('sqlite:///access_project.db')
df_profiles = pd.read_sql('SELECT * FROM patient_profiles', engine)

# Read feedback from MongoDB
client = MongoClient('localhost', 27017)
db = client['access_project']
df_feedback = pd.DataFrame(list(db.feedback.find()))

# Remove MongoDB ObjectId if present
if '_id' in df_feedback.columns:
    df_feedback = df_feedback.drop(columns=['_id'])

# Ensure IDs are integer
df_profiles['patient_id'] = df_profiles['patient_id'].astype(int)
df_feedback['patient_id'] = df_feedback['patient_id'].astype(int)

# Merge datasets
merged_df = pd.merge(df_profiles, df_feedback, on='patient_id', suffixes=('_profile', '_feedback'))

# Clean missing values (if any)
merged_df['satisfaction_score'] = merged_df['satisfaction_score'].fillna(merged_df['satisfaction_score'].mean())

# Save merged data into SQL
merged_df.to_sql('merged_access_data', engine, if_exists='replace', index=False)
print("Merged data stored in SQL as table 'merged_access_data'.")



# --- Configuration ---
st.set_page_config(page_title="Inclusive Digital Healthcare Dashboard 🇪🇺",
                   layout="wide",
                   page_icon="🩺")

st.title("Inclusive Digital Healthcare in Europe")
st.caption("Analytical Visualization of Accessibility Challenges (Sample Project Dashboard)")

# --- Data Load from SQL ---
engine = create_engine('sqlite:///access_project.db')
merged_df = pd.read_sql('SELECT * FROM merged_access_data', engine)

# --- Sidebar Filters ---
st.sidebar.header("Filter Data")
country_list = ['All'] + sorted(merged_df['country_profile'].unique().tolist())
country = st.sidebar.selectbox("Country", country_list)

if country != 'All':
    data = merged_df[merged_df['country_profile'] == country]
else:
    data = merged_df

# --- KPIs ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Patients", f"{data['patient_id'].nunique():,}")
col2.metric("Countries", f"{data['country_profile'].nunique()}")
col3.metric("Accessibility Types", f"{data['accessibility_type'].nunique()}")
col4.metric("Avg. Satisfaction", f"{data['satisfaction_score'].mean():.2f} / 5")

st.write("---")

# --- Plots Section ---
c1, c2 = st.columns([1.2, 1])

# --- Plot 1: Country Distribution ---
with c1:
    st.subheader("Top 10 Patient Populations by Country")
    fig, ax = plt.subplots(figsize=(8,4))
    colors = sns.color_palette("crest", as_cmap=True)
    (data['country_profile'].value_counts().head(10).sort_values()).plot.barh(ax=ax, color=colors(range(10)))
    ax.set_xlabel("Patient Count")
    ax.set_ylabel("Country")
    st.pyplot(fig)

# --- Plot 2: Accessibility Satisfaction ---
with c2:
    st.subheader("Satisfaction Score by Accessibility Type")
    fig2, ax2 = plt.subplots(figsize=(5,4))
    sns.barplot(x=data['accessibility_type'], y=data['satisfaction_score'], ax=ax2, palette="mako", errorbar=None)
    ax2.set_ylabel("Avg. Satisfaction")
    ax2.set_xlabel("Accessibility Type")
    plt.ylim(1,5)
    st.pyplot(fig2)

# --- Row 2 (Demographics & Feedback) ---
c3, c4 = st.columns(2)

with c3:
    st.subheader("Gender Balance")
    gender_counts = data['gender'].value_counts()
    fig3, ax3 = plt.subplots(figsize=(3,3))
    ax3.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%',
            colors=sns.color_palette("pastel"), startangle=150, wedgeprops=dict(width=0.5))
    plt.title("")
    st.pyplot(fig3)

with c4:
    st.subheader("Feedback Issue Types")
    fig4, ax4 = plt.subplots(figsize=(5,3))
    issue_counts = data['issue_type'].value_counts().head(6)
    sns.barplot(y=issue_counts.index, x=issue_counts.values, ax=ax4, hue=issue_counts.index,
                dodge=False, palette="flare")
    ax4.legend([],[], frameon=False)
    ax4.set_xlabel("Count")
    ax4.set_ylabel("Issue Type")
    st.pyplot(fig4)

st.write("---")

# --- Row 3: Age & Device Stats ---
d1, d2 = st.columns(2)
with d1:
    st.subheader("Age Distribution")
    fig5, ax5 = plt.subplots(figsize=(6,2.5))
    sns.histplot(data['age'], bins=20, color="#3984e8")
    ax5.set_xlabel("Age")
    st.pyplot(fig5)

with d2:
    st.subheader("Device Type Usage")
    fig6, ax6 = plt.subplots(figsize=(3,2.5))
    sns.countplot(x="device_type", data=data, palette="viridis", ax=ax6)
    ax6.set_xlabel("Device")
    ax6.set_ylabel("Patients")
    st.pyplot(fig6)

# --- Detailed Data Table ---
with st.expander("🔎 Preview Cleaned Dataset (First 100 Rows)"):
    st.dataframe(data.head(100))

# --- Footer & Branding ---
st.write("---")
st.markdown("""
<small>
Dashboard by <b>Your Team</b> | 
Project: <b>Enabling Inclusive Digital Healthcare Through Analytical Visualization of Accessibility Challenges</b>
</small>
""", unsafe_allow_html=True)

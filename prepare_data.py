import pandas as pd
from sqlalchemy import create_engine

# Load patient profiles from CSV to SQL
df_profiles = pd.read_csv('patient_profiles_europe.csv')
engine = create_engine('sqlite:///access_project.db')
df_profiles.to_sql('patient_profiles', engine, if_exists='replace', index=False)

# Load feedback from CSV to DataFrame
df_feedback = pd.read_csv('feedback_flattened.csv')
if '_id' in df_feedback.columns:
    df_feedback = df_feedback.drop(columns=['_id'])

df_profiles['patient_id'] = df_profiles['patient_id'].astype(int)
df_feedback['patient_id'] = df_feedback['patient_id'].astype(int)

# Merge on patient_id
merged_df = pd.merge(df_profiles, df_feedback, on='patient_id', suffixes=('_profile', '_feedback'))
if 'satisfaction_score' in merged_df.columns:
    merged_df['satisfaction_score'] = merged_df['satisfaction_score'].fillna(merged_df['satisfaction_score'].mean())

# Save merged data into SQL
merged_df.to_sql('merged_access_data', engine, if_exists='replace', index=False)
print("All data saved to SQL database. Ready for dashboard!")

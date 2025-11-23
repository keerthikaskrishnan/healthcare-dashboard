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

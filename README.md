# healthcare-dashboard
An interactive Streamlit app and data pipeline to analyze European healthcare accessibility. Visualizes patient profiles, feedback, and accessibility issues for academic research and stakeholder insights.
# Inclusive Digital Healthcare Dashboard

An interactive Streamlit dashboard for analyzing accessibility challenges in European healthcare.  
This project merges patient profiles and feedback data to uncover important insights for researchers and stakeholders.

## Overview

This app helps visualize and explore healthcare accessibility issues using real-world patient and feedback datasets. It is designed for academic use, professional display, and stakeholder presentations.

## Features

- Interactive and beautiful charts
- Demographic and country analysis
- Accessibility issues and device usage visualization
- Patient satisfaction and feedback exploration
- Easy data filtering and summary statistics

## How to Run

1. **Prepare the Data**  
   Ensure your CSV files (`patient_profiles_europe.csv` and `feedback_flattened.csv`) are in the project folder.

   Run the following command to build the merged database:
#python prepare_data.py
This will create `access_project.db` with all required tables.

2. **Launch the Dashboard**
streamlit run modern_dashboard.py
This will open the dashboard in your web browser.

## Project Files

- `modern_dashboard.py` &mdash; The Streamlit dashboard code
- `prepare_data.py` &mdash; Data merging and database builder
- `patient_profiles_europe.csv` &mdash; Patient demographic data
- `feedback_flattened.csv` &mdash; Accessibility feedback responses
- `requirements.txt` &mdash; Python dependencies
- `README.md` &mdash; Project instructions (this file)

## Deployment

For sharing online (e.g. with your professor):
- Upload all project files to a GitHub repository.
- Deploy on [Streamlit Community Cloud](https://streamlit.io/cloud) for a public link.

## Attribution

Dashboard code inspired by open-source documentation and developed with the assistance of AI tools for educational use.  
All rights reserved to the project author(s).

## License

For academic and educational purposes only. Not for commercial use.

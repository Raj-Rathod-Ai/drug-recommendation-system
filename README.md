# Personalized Medication Advisor - Streamlit App

This is a premium, conversational Streamlit application designed for recommending suitable drugs based on demographic and medical parameters.

## Features & Questionnaire Flow
The application guides the user through a simple 6-step conversational questionnaire:
1. **Age**: Enter user's age in years.
2. **Biological Sex**: Select Male or Female.
3. **Blood Pressure Level**: Choose BP category (Low, Normal, High) or default.
4. **Cholesterol Level**: Choose Cholesterol level (Normal, High) or default.
5. **Sodium-to-Potassium Ratio**: Enter electrolyte ratio (Na_to_K) or use standard default.
6. **Prediction**: Summarizes user's inputs and uses the Decision Tree Classifier to recommend the best drug alongside a confidence probability.

## How to Run Locally

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

## Deploying to Streamlit Community Cloud

1. Push this directory to your GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and connect your repository.
3. Set the main file path to `app.py`.

## Keep-Alive Configuration (No-Sleep Workflow)
Streamlit Community Cloud automatically puts applications to sleep after 7 days of inactivity. 

To keep this application awake continuously:
1. Go to your GitHub repository -> **Settings** -> **Secrets and variables** -> **Actions**.
2. Click **New repository secret**.
3. Name the secret **`APP_URL`**.
4. Set the value to the deployed URL of your Streamlit app (e.g., `https://your-app-name.streamlit.app`).
5. The daily GitHub Action in `.github/workflows/keep_alive.yml` will automatically ping this URL to ensure it never goes to sleep.

📊 Credit Score Analysis & Business Insights Dashboard

An Exploratory Data Analysis (EDA) dashboard built with Streamlit to analyze credit score patterns and uncover actionable business insights for financial decision-making. It highlights how income, payment behavior, utilization, inquiries, and credit history relate to credit scores across a large customer dataset.

🔗 Live Demo
App: https://credit-score-insights.streamlit.app/

🚀 Features
Multi-page Streamlit app with sidebar navigation.

Data Preview with scrollable sample and summary statistics.

Chart Explorer with interactive visuals:

Credit Score Distribution

Income vs Credit Score

Cards vs Credit Score

Delayed Payments vs Credit Score

Seasonal Credit Trends

Payment Behavior by Score

Occupation vs Credit Score

Credit Inquiries by Score

Credit History Age by Score

Spearman Correlation Heatmap

Business Insights page with key findings, strategies, and expected impact.

Bonus page: Credit card usage guide (pitfalls + best practices).


📂 Dataset
100,000+ customer records, 28 features (demographics, financial metrics, credit behavior, payment patterns).

Stored as dataset.csv.gz in the project root for fast, lossless loading.

📦 Tech Stack
Streamlit, Python, Pandas, NumPy, Seaborn, Matplotlib, Plotly.

▶️ Quickstart (Local)
Python 3.12 recommended.

Install dependencies:

pip install -r requirements.txt

Run:

streamlit run app.py

⚙️ Deployment
Pushed to GitHub with requirements.txt and runtime.txt (python-3.12).

Deployed on Streamlit Community Cloud by selecting the repo, branch main, and app.py as entrypoint.

🔑 Key Insights (Examples)
Delayed payments and multiple inquiries correlate negatively with credit score.

Longer credit history and disciplined utilization correlate positively.

Majority of users in the Standard tier → strong upgrade opportunity through education and nudges.

🗂️ Repository Structure
app.py — Streamlit dashboard entrypoint

PaisaBazaar.ipynb — EDA and supporting analysis

dataset.csv.gz — compressed dataset

requirements.txt — dependencies

README.md — this file

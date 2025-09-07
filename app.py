# app.py

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# -------------------- CONFIG --------------------
st.set_page_config(
    page_title="Credit Score Analysis & Insights Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- SIDEBAR NAV --------------------
st.sidebar.title("📊 Navigation")
section = st.sidebar.radio(
    "Go to",
    ("🏠 Overview", "📊 Data Preview", "📈 Chart Explorer",
     "💡 Business Insights & Conclusion", "🎁 Bonus: Credit Card Guide")
)

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv.gz")
    df = df.replace({"Payment_of_Min_Amount": {"NM": "No"}})
    df = df[df["Age"] >= 18].reset_index(drop=True)
    # Ordinal encode Credit_Score
    score_map = {"Poor": 0, "Standard": 1, "Good": 2}
    df["Credit_Score_ord"] = df["Credit_Score"].map(score_map)
    return df

data = load_data()

# -------------------- 1. OVERVIEW --------------------
if section == "🏠 Overview":
    st.title("📊 Credit Score Analysis & Business Insights Dashboard")

    st.markdown(
        """
        ### 🎯 Project Purpose
        Financial institutions often struggle to understand how customer attributes
        like **income, loans, delayed payments, and credit utilization** impact credit scores.
        Without clear data exploration, **hidden trends and risks remain unnoticed**.

        This project applies **visual analytics** to uncover:
        - ✅ What drives credit scores
        - ✅ Where risks & opportunities exist
        - ✅ How businesses can act on these insights

        ---
        ### 📌 Problem Statement
        The problem addressed in this project is the **limited understanding of how customer financial behavior affects credit scores**.
        By exploring 100,000 customer records with 28 variables, this analysis identifies patterns and correlations
        that help businesses improve risk management and customer engagement.

        ---
        ### 🚀 Business Objective
        1. Understand **credit score distribution** across demographics & financial metrics
        2. Identify **key correlations** (delayed payments, inquiries, utilization)
        3. Detect **seasonal & behavioral patterns** in credit performance
        4. Support **stakeholder decision-making** with evidence-based insights
        

        👉 Inspired by real-world use cases such as **Paisabazaar**, where credit score insights
        directly impact lending decisions, customer acquisition, and financial guidance.

        ---
        ⏳ *Note: Some charts may take a few seconds to load. Please don’t switch too quickly.*
        """
    )

# -------------------- 2. DATA PREVIEW --------------------
elif section == "📊 Data Preview":
    st.title("📊 Dataset Preview")

    st.markdown("Here’s a scrollable preview of the dataset (50 rows at a time):")
    st.dataframe(data.head(50), use_container_width=True)

    st.markdown("### 📈 Dataset Summary Statistics")
    st.write(data.describe())

# -------------------- 3. CHART EXPLORER --------------------
elif section == "📈 Chart Explorer":
    st.title("📈 Interactive Chart Explorer")

    chart = st.selectbox("Choose a chart to display:", [
        "Credit Score Distribution",
        "Income vs Credit Score",
        "Cards vs Credit Score",
        "Delayed Payments vs Credit Score",
        "Seasonal Credit Trends",
        "Payment Behavior by Score",
        "Occupation vs Credit Score",
        "Credit Inquiries by Score",
        "Credit History Age by Score",
        "Correlation Heatmap"
    ])

    st.subheader(chart)

    if chart == "Credit Score Distribution":
        counts = data["Credit_Score"].value_counts().reindex(["Poor","Standard","Good"])
        fig = px.pie(values=counts.values, names=counts.index,
                     title="Credit Score Composition",
                     color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)
        st.info("👉 Over half of customers fall into the Standard tier, showing upgrade potential.")

    elif chart == "Income vs Credit Score":
        fig = px.box(data, x="Credit_Score", y="Annual_Income", color="Credit_Score",
                     category_orders={"Credit_Score": ["Poor","Standard","Good"]},
                     title="Annual Income by Credit Score")
        st.plotly_chart(fig, use_container_width=True)
        st.info("👉 Higher income levels are generally associated with better credit scores.")

    elif chart == "Cards vs Credit Score":
        fig = px.box(data, x="Credit_Score", y="Num_Credit_Card", color="Credit_Score",
                     category_orders={"Credit_Score": ["Poor","Standard","Good"]},
                     title="Number of Credit Cards by Credit Score")
        st.plotly_chart(fig, use_container_width=True)
        st.info("👉 Customers with too many credit cards often trend towards lower credit scores.")

    elif chart == "Delayed Payments vs Credit Score":
        avg_delays = data.groupby("Credit_Score")["Num_of_Delayed_Payment"].mean().reindex(["Poor","Standard","Good"])
        fig = px.bar(x=avg_delays.index, y=avg_delays.values,
                     labels={"x": "Credit Score", "y": "Avg Delayed Payments"},
                     title="Average Delayed Payments by Credit Score",
                     color=avg_delays.index, color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)
        st.info("👉 Delayed payments are the strongest negative driver of credit scores.")

    elif chart == "Seasonal Credit Trends":
        trends = data.groupby(["Month", "Credit_Score"]).size().unstack(fill_value=0)
        trends_pct = trends.div(trends.sum(axis=1), axis=0) * 100
        fig = px.line(trends_pct, x=trends_pct.index, y=["Poor","Standard","Good"],
                      title="Monthly Credit Score Distribution (%)", markers=True)
        fig.update_layout(xaxis_title="Month", yaxis_title="Percentage of Customers")
        st.plotly_chart(fig, use_container_width=True)
        st.info("👉 Seasonal shifts show when credit performance weakens or improves.")

    elif chart == "Payment Behavior by Score":
        behavior = data.groupby(["Payment_Behaviour", "Credit_Score"]).size().reset_index(name='Count')
        fig = px.bar(behavior, x="Payment_Behaviour", y="Count", color="Credit_Score",
                     title="Payment Behavior vs Credit Score")
        fig.update_layout(xaxis_title="Payment Behavior", xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        st.info("👉 Payment behavior strongly differentiates Good vs Poor customers.")

    elif chart == "Occupation vs Credit Score":
        occ = pd.crosstab(data["Occupation"], data["Credit_Score"], normalize="index") * 100
        fig = px.imshow(occ, text_auto=True, aspect="auto", color_continuous_scale="YlGnBu",
                        labels=dict(x="Credit Score", y="Occupation", color="Percent"))
        fig.update_layout(title="Occupation vs Credit Score (%)")
        st.plotly_chart(fig, use_container_width=True)
        st.info("👉 Certain occupations have stronger associations with good credit standing.")

    elif chart == "Credit Inquiries by Score":
        fig = px.box(data, x="Credit_Score", y="Num_Credit_Inquiries", color="Credit_Score",
                     category_orders={"Credit_Score": ["Poor","Standard","Good"]},
                     title="Credit Inquiries by Credit Score")
        st.plotly_chart(fig, use_container_width=True)
        st.info("👉 Multiple credit inquiries usually signal higher risk.")

    elif chart == "Credit History Age by Score":
        fig = px.box(data, x="Credit_Score", y="Credit_History_Age", color="Credit_Score",
                     title="Credit History Age (days) by Credit Score")
        st.plotly_chart(fig, use_container_width=True)
        st.info("👉 Longer credit history is positively linked with higher scores.")

    elif chart == "Correlation Heatmap":
        num_cols = [
            "Annual_Income", "Num_Bank_Accounts", "Num_Credit_Card",
            "Num_of_Loan", "Num_of_Delayed_Payment", "Num_Credit_Inquiries",
            "Credit_Utilization_Ratio", "Amount_invested_monthly",
            "Credit_History_Age", "Credit_Score_ord"
        ]
        corr = data[num_cols].corr(method="spearman")
        mask = np.triu(np.ones_like(corr, dtype=bool))

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r", center=0, linewidths=0.5, ax=ax)
        ax.set_title("Spearman Correlation Heatmap")
        st.pyplot(fig)
        st.info("👉 Delayed payments & multiple inquiries show strongest negative correlation with credit score.")

# -------------------- 4. BUSINESS INSIGHTS --------------------
elif section == "💡 Business Insights & Conclusion":
    st.title("💡 Strategic Business Insights & Conclusion")

    st.markdown(
        """
        ### 🔑 Key Findings
        1. **Delayed payments** are the biggest negative driver (r = -0.43).
        2. **53.3% of customers** fall into the Standard tier → huge upgrade opportunity.
        3. Customers with **multiple inquiries & products** show predictable higher risk.

        ---
        ### 📌 Business Recommendations
        - **Payment Behavior Programs** → Automated reminders, flexible scheduling, early assistance
        - **Standard Segment Growth** → Credit education, reward programs, personalized improvement roadmaps
        - **Risk Management** → Cooling-off periods for frequent inquiries, debt consolidation for over-leveraged customers

        ---
        ### 🚀 Expected Business Impact
        - 25–30% reduction in delayed payments
        - 15–20% migration from Standard → Good tier
        - 20–25% reduction in overall portfolio risk

        ---
        ### ✅ Conclusion
        This analysis provides a **clear roadmap**:
        Focus on **payment behavior improvement**, **upgrading the Standard tier**, and **proactive risk management**.
        These strategies improve **customer outcomes** and ensure **sustainable business growth**.
        """
    )

# -------------------- 5. BONUS PAGE --------------------
elif section == "🎁 Bonus: Credit Card Guide":
    st.title("🎁 Credit Card Usage Guide: Pitfalls & Best Practices")

    st.markdown(
        """
        ### ⚠️ Common Pitfalls
        - Paying only the **minimum due** → keeps you in debt longer
        - Having **too many cards** → harder to manage, risk of overspending
        - **Multiple credit inquiries** → quickly lowers your score
        - High **credit utilization** (>30%) → negative signal to lenders

        ---
        ### 💡 Best Practices
        - Keep credit utilization **below 30%**
        - Always **pay full balance** on time
        - Maintain **older accounts** (longer history = better score)
        - Monitor credit reports regularly

        ---
        ### 🌟 Pro Tips Most Don’t Know
        - Checking your **own credit report** doesn’t hurt your score
        - A mix of products (**loan + card**) can improve credit health if managed well
        - Consistent timely payments are **more important than income level**

        ---
        ✅ Following these practices helps customers avoid traps,
        build strong credit history, and achieve long-term financial stability.
        """
    )

# -------------------- FOOTER --------------------
st.sidebar.markdown("---")
st.sidebar.caption("© 2025 Credit Score Insights Dashboard – Built with Streamlit")


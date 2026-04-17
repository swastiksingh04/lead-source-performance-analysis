import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

st.title("📊 Lead Source Performance Dashboard")

# ================================
# LOAD DATA
# ================================
leads = pd.read_csv("leads.csv")
funnel = pd.read_csv("funnel.csv")
cost = pd.read_csv("cost.csv")

df = leads.merge(funnel, on="Lead_ID")

# ================================
# SIDEBAR FILTERS
# ================================
st.sidebar.header("📌 Filters")

selected_sources = st.sidebar.multiselect(
    "Select Lead Source",
    df["Lead_Source"].unique(),
    default=df["Lead_Source"].unique()
)

selected_city = st.sidebar.multiselect(
    "Select City",
    df["City"].unique(),
    default=df["City"].unique()
)

# APPLY FILTERS
filtered_df = df[
    (df["Lead_Source"].isin(selected_sources)) &
    (df["City"].isin(selected_city))
]

# ================================
# PROCESS DATA (AFTER FILTER)
# ================================
lead = filtered_df.groupby("Lead_Source")["Lead_ID"].nunique()
application = filtered_df[filtered_df["Application"] == "Yes"].groupby("Lead_Source")["Lead_ID"].count()
enrollments = filtered_df[filtered_df["Enrolled"] == "Yes"].groupby("Lead_Source")["Lead_ID"].count()

analysis = pd.DataFrame({
    "Leads": lead,
    "Applications": application,
    "Enrollments": enrollments
}).fillna(0)

analysis["Conversion_Rate"] = (analysis["Enrollments"] / analysis["Leads"] * 100).round(2)
analysis = analysis.reset_index()

analysis = analysis.merge(cost, left_on="Lead_Source", right_on="Channel")

analysis["Cost_per_Lead"] = (analysis["Monthly_Cost"] / analysis["Leads"]).round(2)
analysis["Cost_per_Enrollment"] = (analysis["Monthly_Cost"] / analysis["Enrollments"]).round(2)

# ================================
# KPI CARDS 🔥
# ================================
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Leads", int(analysis["Leads"].sum()))
col2.metric("Total Enrollments", int(analysis["Enrollments"].sum()))
col3.metric("Avg Conversion %", round(analysis["Conversion_Rate"].mean(), 2))

# ================================
# BAR CHART & PIE CHART (SIDE BY SIDE)
# ================================
st.subheader("📈 Performance by Lead Source & 🥧 Lead Distribution")

col_left, col_right = st.columns(2)

with col_left:
    metric = st.selectbox(
        "Choose Metric",
        ["Leads", "Applications", "Enrollments", "Conversion_Rate", "Cost_per_Enrollment"]
    )
    
    fig, ax = plt.subplots(figsize=(5, 3.5))
    sns.barplot(x="Lead_Source", y=metric, data=analysis, ax=ax)
    
    for i, v in enumerate(analysis[metric]):
        ax.text(i, v, str(round(v, 2)), ha='center', va='bottom', fontsize=8)
    
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

with col_right:
    lead_share = filtered_df["Lead_Source"].value_counts()
    
    fig2, ax2 = plt.subplots(figsize=(5, 3.5))
    ax2.pie(lead_share, labels=lead_share.index, autopct='%1.1f%%', textprops={'fontsize': 9})
    plt.tight_layout()
    st.pyplot(fig2)

# ================================
# HEATMAP & SCATTER PLOT (SIDE BY SIDE)
# ================================
st.subheader("🔥 Correlation Matrix & 🎯 Conversion vs Cost")

col_left2, col_right2 = st.columns(2)

with col_left2:
    corr = analysis[
        ["Leads", "Applications", "Enrollments",
         "Conversion_Rate", "Monthly_Cost", "Cost_per_Enrollment"]
    ].corr()
    
    fig3, ax3 = plt.subplots(figsize=(5, 4))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax3, fmt=".2f", cbar_kws={'label': 'Correlation'})
    plt.tight_layout()
    st.pyplot(fig3)

with col_right2:
    fig4, ax4 = plt.subplots(figsize=(5, 4))
    ax4.scatter(analysis["Conversion_Rate"], analysis["Cost_per_Enrollment"], s=100, alpha=0.6)
    
    for i, txt in enumerate(analysis["Lead_Source"]):
        ax4.text(
            analysis["Conversion_Rate"][i],
            analysis["Cost_per_Enrollment"][i],
            txt,
            fontsize=8,
            ha='center'
        )
    
    ax4.set_xlabel("Conversion Rate (%)")
    ax4.set_ylabel("Cost per Enrollment ($)")
    ax4.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig4)

# ================================
# TOP PERFORMER 🔥
# ================================
st.subheader("🏆 Best Performing Source")

best = analysis.sort_values(by="Conversion_Rate", ascending=False).iloc[0]

st.success(
    f"🎯 {best['Lead_Source']} has the highest conversion rate ({best['Conversion_Rate']}%)"
)
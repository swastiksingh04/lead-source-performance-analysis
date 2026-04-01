import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

leads=pd.read_csv("leads.csv")
funnel=pd.read_csv("funnel.csv")
cost=pd.read_csv("cost.csv")

df=leads.merge(funnel, on="Lead_ID")
print(df.head(10))

print(cost.columns)
print(df.columns)

lead = df.groupby("Lead_Source")["Lead_ID"].nunique()

application = df[df["Application"]=="Yes"].groupby("Lead_Source")["Lead_ID"].count()

enrollments = df[df["Enrolled"]=="Yes"].groupby("Lead_Source")["Lead_ID"].count()

analysis = pd.DataFrame({
    "Leads": lead,
    "Applications": application,
    "Enrollments": enrollments
})

analysis["Conversion_Rate"] = (analysis["Enrollments"] / analysis["Leads"] * 100).round(2)
print(analysis)

analysis = analysis.reset_index()

analysis = analysis.merge(cost, left_on="Lead_Source", right_on="Channel")

analysis["Cost_per_Lead"] = (analysis["Monthly_Cost"] / analysis["Leads"]).round(2)
analysis["Cost_per_Enrollment"] = (analysis["Monthly_Cost"] / analysis["Enrollments"]).round(2)

print(analysis)

quality = df[df["Test_Score"].notna()].groupby("Lead_Source")["Test_Score"].mean().round(2).reset_index()

quality.columns = ["Lead_Source", "Avg_Test_Score"]

print(quality)

course_demand = df.groupby(["Lead_Source", "Course_Interest"])["Lead_ID"].count().reset_index()

course_demand.columns = ["Lead_Source", "Course", "Count"]
print(course_demand)

city_analysis = df.groupby(["City", "Lead_Source"])["Lead_ID"].count().reset_index()
print(city_analysis)

df["Date"] = pd.to_datetime(df["Date"],dayfirst=True)

trend = df.groupby(df["Date"].dt.to_period("M"))["Lead_ID"].count()
print(trend)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

ax1 = axes[0]
analysis.plot(x="Lead_Source", y="Conversion_Rate", kind="bar", ax=ax1, legend=False)
ax1.set_title("Conversion Rate (%)")

for i, v in enumerate(analysis["Conversion_Rate"]):
    ax1.text(i, v + 0.5, str(v), ha='center')

ax2 = axes[1]
analysis.plot(x="Lead_Source", y="Cost_per_Enrollment", kind="bar", ax=ax2, legend=False)
ax2.set_title("Cost per Enrollment")

for i, v in enumerate(analysis["Cost_per_Enrollment"]):
    ax2.text(i, v + 5, str(v), ha='center')

plt.tight_layout()
plt.show()

plt.figure(figsize=(6,4))

plt.bar(quality["Lead_Source"], quality["Avg_Test_Score"])
plt.title("Average Test Score")

for i, v in enumerate(quality["Avg_Test_Score"]):
    plt.text(i, v + 0.5, str(v), ha='center')

plt.show()

lead_share = analysis.set_index("Lead_Source")["Leads"]

plt.figure(figsize=(6,6))

plt.pie(lead_share, labels=lead_share.index, autopct='%1.1f%%')
plt.title("Lead Source Share")

plt.show()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].bar(analysis["Lead_Source"], analysis["Conversion_Rate"])
axes[0].set_title("Conversion Rate (%)")
axes[0].set_xlabel("Lead Source")

for i, v in enumerate(analysis["Conversion_Rate"]):
    axes[0].text(i, v + 0.5, str(v), ha='center')

axes[1].bar(analysis["Lead_Source"], analysis["Cost_per_Enrollment"])
axes[1].set_title("Cost per Enrollment")
axes[1].set_xlabel("Lead Source")

for i, v in enumerate(analysis["Cost_per_Enrollment"]):
    axes[1].text(i, v + 20, str(v), ha='center')

plt.tight_layout()
plt.show()

corr = analysis[["Leads", "Enrollments", "Conversion_Rate", "Monthly_Cost", "Cost_per_Enrollment"]].corr()

plt.figure(figsize=(6,4))

sns.heatmap(corr, annot=True, cmap="coolwarm")

plt.title("Correlation Matrix")
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 🔹 Conversion vs Cost
axes[0].scatter(analysis["Conversion_Rate"], analysis["Cost_per_Enrollment"])
axes[0].set_title("Conversion vs Cost")
axes[0].set_xlabel("Conversion Rate (%)")
axes[0].set_ylabel("Cost per Enrollment")

for i, txt in enumerate(analysis["Lead_Source"]):
    axes[0].text(analysis["Conversion_Rate"][i], analysis["Cost_per_Enrollment"][i], txt)

# 🔹 Leads vs Enrollments
axes[1].scatter(analysis["Leads"], analysis["Enrollments"])
axes[1].set_title("Leads vs Enrollments")
axes[1].set_xlabel("Leads")
axes[1].set_ylabel("Enrollments")

for i, txt in enumerate(analysis["Lead_Source"]):
    axes[1].text(analysis["Leads"][i], analysis["Enrollments"][i], txt)

plt.tight_layout()
plt.show()

merged = analysis.merge(quality, on="Lead_Source")

plt.figure(figsize=(6,4))

plt.scatter(merged["Avg_Test_Score"], merged["Conversion_Rate"])

for i, txt in enumerate(merged["Lead_Source"]):
    plt.text(merged["Avg_Test_Score"][i], merged["Conversion_Rate"][i], txt)

plt.xlabel("Avg Test Score")
plt.ylabel("Conversion Rate")
plt.title("Quality vs Conversion")

plt.show()
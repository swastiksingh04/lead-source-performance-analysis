# 📊 Lead Source Performance & Funnel Analysis

## 🚀 Overview

This project analyzes the effectiveness of different lead acquisition channels such as LinkedIn, Instagram, Website, and Campus Drives.
It focuses on understanding conversion performance, cost efficiency, and student quality across the complete funnel.

The project also includes a Streamlit dashboard for interactive visualization.

---

## 🎯 Objectives

* Analyze lead generation performance across channels
* Evaluate funnel stages (Leads → Applications → Enrollments)
* Calculate conversion rates
* Perform cost analysis (Cost per Lead & Cost per Enrollment)
* Analyze student quality using test scores
* Identify most efficient marketing channels

---

## 📂 Dataset

Real dataset (~15,000 records) with the following tables:

### 1. Leads Data

* Lead_ID
* Lead_Source
* City
* Course_Interest
* Date
* Test_Score *(available only for enrolled students)*

### 2. Funnel Data

* Lead_ID
* Counselling
* Application
* Enrolled

### 3. Cost Data

* Channel
* Monthly_Cost

---

## 📈 Key Analysis Performed

### 🔹 Funnel Analysis

* Leads → Applications → Enrollments
* Conversion rate calculation

### 🔹 Cost Analysis

* Total cost per channel
* Cost per Lead
* Cost per Enrollment

### 🔹 Performance Analysis

* Best performing lead source
* Channel-wise comparison

### 🔹 Student Quality Analysis

* Average test score per channel
* Quality vs conversion insights

### 🔹 Correlation Analysis

* Conversion Rate vs Cost
* Leads vs Enrollments

---

## 📊 Visualizations

* Bar charts (Conversion Rate, Cost Analysis)
* Pie chart (Lead Source Distribution)
* Time series (Leads over time)
* Subplots for comparative analysis
* Scatter plots for correlation

---

## 🖥️ Dashboard (Streamlit)

An interactive dashboard is built using Streamlit to:

* Filter data by channel
* Visualize KPIs
* Compare performance dynamically

---

## 🛠️ Tech Stack

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Streamlit

---

## 📌 Key Insights

* LinkedIn shows highest conversion rate
* Instagram generates highest leads volume
* Website provides balanced performance
* Cost efficiency varies significantly across channels
* High-quality students are not always from highest lead sources

---

## ▶️ How to Run

### 1. Clone repo

git clone https://github.com/your-username/lead-source-performance-analysis.git
cd lead-source-performance-analysis

### 2. Install dependencies

pip install pandas numpy matplotlib seaborn streamlit

### 3. Run analysis

Lead_Source_Performance_Analysis.py

### 4. Run dashboard

streamlit_app.py

---

## 📌 Future Improvements

* Predictive modeling (lead conversion prediction)
* ROI optimization using ML
* Automated reporting

---

## 👨‍💻 Contributors

* Swastik Singh

---

## ⭐ If you like this project, give it a star!

# Toronto Bike Sharing Demand Prediction & Analytics

End-to-end data analytics and predictive modeling project analyzing Toronto bike-sharing usage patterns using regression techniques and interactive dashboards.

---

## Project Overview

This project analyzes bike-sharing demand in Toronto to identify usage patterns and build predictive models for ride demand.

The analysis combines exploratory data analysis, feature engineering, regression modeling, and business insights to support operational decision-making.

---

## Business Problem

Bike-sharing systems require accurate demand forecasting to:

* Optimize bike availability
* Improve station distribution
* Reduce shortages and idle capacity
* Enhance user experience

---

## Objectives

* Analyze historical bike-sharing usage patterns
* Identify key drivers of demand (time, weather, seasonality)
* Build predictive models for ride demand
* Provide actionable business insights

---

## Key Insights

* Demand peaks during **rush hours (morning & evening)**
* Weather significantly impacts usage (temperature, rain)
* Seasonal patterns show higher usage in warmer months
* Weekdays and weekends show distinct usage behavior

---

## Modeling Approach

* Feature Engineering:

  * Hour, day, month
  * Temperature, humidity
  * Seasonal indicators

* Models:

  * Linear Regression
  * Random Forest
  * XGBoost

* Evaluation Metrics:

  * RMSE
  * R² Score

---

## Streamlit Dashboard

Run locally:

```bash
streamlit run app/Home.py
```

---

## Project Structure

```
toronto-bike-sharing-analytics/
├── app/
├── src/
├── data/
├── figures/
├── reports/
├── tests/
├── notebooks/
└── README.md
```

---

## Tools and Technologies

* Python (Pandas, NumPy, Scikit-learn, XGBoost)
* Matplotlib, Seaborn
* Streamlit
* Data preprocessing and modeling techniques

---

## Key Takeaways

* Demand is highly time-dependent (hour + season)
* Weather is a critical influencing factor
* Predictive models can significantly support operations
* Data-driven insights improve resource allocation

---

## Author

Roberto Alberto San Miguel
Master of Data Analytics – Niagara Falls University

---

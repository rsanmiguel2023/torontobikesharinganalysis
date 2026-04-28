# Toronto Bike Sharing Analytics Dashboard

End-to-end Python analytics project for exploring Toronto bike-sharing trip patterns, station usage, user behavior, and dashboard-ready operational KPIs. The project is organized in a clean portfolio format with modular source code, tests, reports, figures, and a Streamlit dashboard.

---

## Project Overview

This project analyzes bike-sharing trip data to help understand ridership behavior, station demand, trip duration patterns, user type differences, and operational usage trends.

The project was converted into a portfolio-ready GitHub repository using a production-style structure similar to a capstone analytics project. It includes reusable Python modules, test coverage, technical documentation, and an interactive Streamlit application.

---

## Business Problem

Bike-sharing operators need reliable insights to improve service availability, station planning, and customer experience. Without data-driven monitoring, operators may face bike shortages, uneven station usage, poor rebalancing decisions, and reduced rider satisfaction.

This project addresses the following business questions:

- Which stations generate the highest trip volume?
- What are the main usage patterns by user type?
- How long are typical trips?
- When does bike demand peak?
- What KPIs should operators monitor for daily decision-making?

---

## Objectives

- Build a reusable analytics pipeline for bike-sharing trip data
- Clean and process trip-level records
- Generate operational KPIs for dashboard reporting
- Analyze station usage, user types, trip duration, and peak demand
- Create a Streamlit dashboard for interactive exploration
- Add tests to support reliability and maintainability

---

## Key Features

- Data loading and cleaning utilities
- Trip duration analysis
- Station usage ranking
- User type breakdown
- Peak usage analysis
- KPI calculation module
- Interactive dashboard filters
- Reusable visualization functions
- Unit tests for analytics and processing modules

---

## Streamlit Dashboard

Run locally:

```bash
streamlit run app/Home.py
```

Dashboard pages:

- Home: project overview and KPI summary
- EDA: trip patterns, duration distribution, and user mix
- Station Usage: top start stations and demand concentration
- User Type Analysis: annual vs casual member behavior
- Operational Insights: recommendations for operators

---

## Project Structure

```text
toronto-bike-sharing-analytics/
│
├── app/                 # Streamlit dashboard
│   ├── Home.py
│   ├── pages/
│   └── utils/
│
├── src/                 # Core analytics and processing modules
│   ├── analytics/
│   ├── data_processing/
│   ├── utils/
│   └── visualization/
│
├── data/                # Sample, raw, and processed data
├── figures/             # Exported charts and dashboard figures
├── reports/             # Technical documentation
├── tests/               # Unit tests
├── examples/            # Example scripts
│
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## Tools and Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Plotly
- Streamlit
- Pytest

---

## How to Run

```bash
git clone https://github.com/your-username/toronto-bike-sharing-analytics.git
cd toronto-bike-sharing-analytics

pip install -r requirements.txt
streamlit run app/Home.py
```

Run tests:

```bash
python -m pytest -q
```

---

## Key Takeaways

- Bike-sharing demand is highly dependent on station location and time-based usage patterns
- User type analysis helps separate commuter-style usage from casual riding behavior
- Trip duration metrics support operational monitoring and anomaly detection
- Dashboard KPIs help translate raw trip records into practical business insights

---

## Author

Roberto Alberto San Miguel  
Master of Data Analytics – Niagara Falls University

---

## Portfolio Note

This project demonstrates practical skills in data processing, exploratory analysis, dashboard development, modular Python design, and test-driven analytics workflows.

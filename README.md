🚗 Traffic Accident Hotspot Reporter

An interactive data analytics dashboard built with Python, Pandas, Plotly, and Streamlit to analyze road accident data, generate key safety insights, and visualize accident trends through an intuitive interface.

The application is designed to work with any replacement CSV file that follows the same data schema.

---

## Dashboard Preview

![Dashboard](assets/dashboard_preview.PNG)

## Overview

Traffic Accident Hotspot Reporter is a Python-based data analytics application that transforms raw road accident records into meaningful insights.

The project performs automated data cleaning and validation, generates safety KPIs, identifies accident hotspots, and presents the results through an interactive Streamlit dashboard.

The application is designed to work with replacement datasets that follow the same data schema, making it reusable for future analyses.

# Features

## Data Cleaning

* Load accident records from CSV
* Validate required columns
* Parse accident dates
* Remove duplicate records
* Handle missing values
* Generate month column for trend analysis

---

## KPI Dashboard

Displays the following Key Performance Indicators (KPIs):

* Total Accidents
* Severe Accidents
* Peak Accident Hour
* Top Accident Hotspot

---

## Interactive Charts

* Accident Frequency by Hour
* Severity by Road Type
* Monthly Accident Trend
* Accident Count by Weather Condition

---

## Hotspot Ranking

Displays hotspot rankings including:

* Location Name
* Zone
* Total Accident Count
* Severe Accident Count

---

## Filters

The dashboard supports interactive filtering by:

* Date Range
* Severity
* Road Type
* Weather Condition
* Zone

---

## Export Reports

Generate downloadable CSV reports for:

* Cleaned Accident Records
* Summary Metrics
* Hotspot Ranking

---

# Project Structure

```
RoadSense/
│
├── assets/
│   └── roadsense_accident_records_raw_v1.csv
│
├── outputs/
│   ├── roadsense_cleaned_records_v1.csv
│   ├── roadsense_summary_metrics_v1.csv
│   └── roadsense_hotspot_ranking_v1.csv
│
├── tests/
│   └── test_roadsense_v1.py
│
├── config.py
├── roadsense_data_cleaning_v1.py
├── roadsense_kpi_engine_v1.py
├── roadsense_chart_engine_v1.py
├── roadsense_dashboard_v1.py
├── requirements.txt
└── README.md
```

---

# Installation

Clone or download the project folder.

Create a virtual environment (recommended):

```
python -m venv .venv
```

Activate the virtual environment.

Windows:

```
.venv\Scripts\activate
```

Linux/macOS:

```
source .venv/bin/activate
```

Install the required packages:

```
pip install -r requirements.txt
```

---

# Running the Project

## Step 1 – Generate Cleaned Data

Run:

```
python roadsense_data_cleaning_v1.py
```

This generates:

* roadsense_cleaned_records_v1.csv

---

## Step 2 – Generate Summary Metrics

Run:

```
python roadsense_kpi_engine_v1.py
```

This generates:

* roadsense_summary_metrics_v1.csv
* roadsense_hotspot_ranking_v1.csv

---

## Step 3 – Launch the Dashboard

Run:

```
streamlit run roadsense_dashboard_v1.py
```

The dashboard will open automatically in your default web browser.

---

# Running Unit Tests

Execute the following command:

```
pytest tests/test_roadsense_v1.py -v
```

Expected output:

```
7 passed
```

---

# Replacing the Input CSV

The application supports replacement datasets.

To use another dataset:

1. Replace the file inside the **assets** folder.
2. Keep the filename:

```
roadsense_accident_records_raw_v1.csv
```

Alternatively, update the file path in **config.py**.

The replacement dataset must contain the same column structure as the original dataset.

Required columns:

* accident_id
* accident_date
* hour_of_day
* location_name
* zone
* road_type
* severity
* weather_condition

Optional columns:

* latitude
* longitude

---

# Technologies Used

* Python 3.10+
* Streamlit
* Pandas
* Plotly
* Pytest

---

# Offline Operation

This project runs completely offline.

No external APIs, cloud services, databases, or web scraping are used.

---

# License

This project was developed as a custom software solution for the Traffic Accident Hotspot Reporter project.

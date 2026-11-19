# Air Quality India – National Air Quality Analytics Dashboard

A district-level air quality analytics dashboard for India that provides historical pollution analysis, pollutant monitoring, AQI estimation, and next-day PM2.5 forecasting.

**Live Dashboard:** https://india-air-quality-monitor.streamlit.app/  
**GitHub Repository:** https://github.com/AmanPatel470/air-quality-india

## Project Overview

Air Quality India is a data-driven dashboard designed to help users explore air pollution trends across Indian states and districts. It collects historical air quality data, processes pollutant measurements, estimates AQI using PM2.5 concentrations, and provides a next-day PM2.5 forecast.

The application combines automated data collection, data processing, visualization, and machine learning to make air quality information easier to understand.

## Dataset Overview

| Metric | Details |
|---|---|
| Geographic Coverage | 728 districts |
| States and Union Territories | 36 |
| Historical Records | 197K+ |
| Data Format | CSV |
| Data Source | Open-Meteo Air Quality API |
| Pollutants | PM2.5, PM10, CO, NO2, O3 |
| Historical Coverage | November 16, 2025 – November 18, 2026 |
| Dataset Size | Approximately 23 MB |

## Key Features

### 1. District-Level Air Quality Monitoring
- Explore air quality information across 728 Indian districts.
- Select states and districts to view location-specific pollution data.
- View estimated AQI values and corresponding air quality categories.

### 2. Pollutant Analysis
- Monitor five major air pollutants: PM2.5, PM10, CO, NO2, and O3.
- Explore pollutant concentrations through interactive visualizations.
- Compare pollutant levels across different locations.

### 3. Historical Air Quality Analysis
- Analyze historical air quality trends using collected daily records.
- Explore changes in pollutant concentrations over time.
- Visualize historical pollution patterns through interactive charts.

### 4. Next-Day PM2.5 Forecasting
- Predict next-day PM2.5 concentrations using a machine learning model.
- Present forecast results to help users understand potential changes in air quality.

### 5. Interactive Dashboard
- Searchable state and district selection.
- Interactive charts and data visualizations.
- Custom dark-themed dashboard interface.
- District-level pollution insights in one place.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn, Random Forest |
| Data Visualization | Plotly |
| Dashboard | Streamlit |
| Data Source | Open-Meteo Air Quality API |
| API Integration | REST API, Requests |
| Automation | GitHub Actions |
| Version Control | Git, GitHub |
| Deployment | Streamlit Community Cloud |

## Data Collection and Processing

The project uses the Open-Meteo Air Quality API to collect historical air quality information for Indian districts.

The data pipeline performs the following operations:

1. Retrieves pollutant measurements for district coordinates.
2. Collects hourly pollutant observations.
3. Aggregates hourly measurements into daily averages.
4. Cleans and processes the collected data using Pandas.
5. Merges newly collected records with the existing historical dataset.
6. Removes duplicate records and maintains an organized dataset.
7. Calculates a PM2.5-based AQI estimate and its corresponding category.

## Automated Data Updates

GitHub Actions is used to automate the data collection and dataset update process.

The workflow:
- Executes the Python data collection script.
- Retrieves the existing historical dataset.
- Fetches the latest available pollutant observations.
- Merges new records with historical data.
- Removes duplicate entries.
- Updates the dataset stored in GitHub Releases.

This reduces the need for manual data collection and helps keep the dashboard's dataset updated.

## Running the Project Locally

### Prerequisites

- Python 3.10 or later
- Git
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/AmanPatel470/air-quality-india.git
```

### 2. Navigate to the Project Directory

```bash
cd air-quality-india
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Dashboard

```bash
streamlit run app/main.py
```

The application will open in your browser.

## Limitations

- AQI values are estimated using PM2.5 concentrations and should not be interpreted as official CPCB AQI measurements, which consider multiple pollutant sub-indices.
- Air quality observations are sourced from Open-Meteo's atmospheric data and are not direct readings from local monitoring stations.
- Data availability and update frequency depend on the external API.
- Forecast results are model-based estimates and should not be treated as guaranteed future measurements.

## Future Enhancements

- Interactive India map with district-level AQI visualization.
- Extended forecasting for multiple days.
- Additional machine learning models for improved forecasting.
- Health advisory recommendations based on air quality categories.
- More detailed state-wise and district-wise comparisons.

## Project Status

**Completed and Deployed**

The dashboard is publicly available, with historical air quality analytics, pollutant monitoring, next-day PM2.5 forecasting, and an automated data collection workflow.

## Author

**Aman Patel**

- GitHub: https://github.com/AmanPatel470
- Live Project: https://india-air-quality-monitor.streamlit.app/

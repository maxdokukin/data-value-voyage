# Value Voyage – A Journey Through Decades of Prices

An interactive dashboard that brings Consumer Price Index (CPI) and purchasing-power data to life by showing how many everyday goods (eggs, bread, housing, gas) an average American could afford each month from 1900 through 2020.  

<p align="center">
  <a href="https://value-voyage-cs163.uw.r.appspot.com">
    <img src="https://github.com/user-attachments/assets/4117cec6-2801-477f-b915-c5d53b949b76" alt="Value Voyage Screenshot" width="800"/>
  </a>
</p>

**Live site:** <https://value-voyage-cs163.uw.r.appspot.com>

---

## Quick Setup

1. **Clone the repo**  
   ```bash
   git clone https://github.com/ryanfernald/Value-Voyage
   cd value-voyage
   ```

2. **Create a virtual environment & install dependencies**  
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3**Run the app locally**  
   ```bash
   python app.py
   ```
   Then visit <http://localhost:5000> in your browser.

---

## Data Pipeline Overview

1. **Ingest & Store**  
   - Raw CPI, income, and housing CSV files in `data/raw/`  
   - `src/insert/` scripts clean & normalize, then write to SQLite (`data/db/database.sqlite`)

2. **Fetch & Aggregate**  
   - `src/fetch/` modules read from local CSV, SQLite, or Google Cloud Storage (based on your config)  
   - Output is a curated DataFrame of quantities, inequality metrics, and housing costs

3. **Visualize**  
   - `src/visualize/` generates Plotly figures 

4. **Serve the Website**  
   - `app.py` wires everything together using Flask (or your chosen framework)  
   - Individual pages are defined in `pages/`:
     - `pages/landing/` – Home overview  
     - `pages/methods/` – Methodologies deep dive  
     - `pages/more/` – Additional context  
     - `pages/findings.py` & `pages/objectives.py` – Core narrative sections  

---

## Repository Structure

```
Value-Voyage/
├── app.yaml                 # GCP App Engine config
├── app.py                   # Main application entrypoint
├── requirements.txt
├── README.md
│
├── components/              # Reusable UI widgets
│   ├── button.py
│   └── topbar.py
│
├── data/
│   ├── raw/                 # Original CSV exports
│   ├── csv/                 # Staged CSVs for ingestion
│   ├── db/                  # SQLite database files
│   └── ryans_data/          # Supplementary datasets
│
├── doc/                     # Architecture docs, diagrams, figures
│   ├── diagrams/
│   └── figures/
│
├── pages/                   # Website page layouts
│   ├── landing/
│   ├── methods/
│   ├── more/
│   ├── findings.py
│   └── objectives.py
│
├── src/
│   ├── db/                  # Database migration from mySQL to sqlite
│   ├── fetch/               # Data‐fetching & aggregation modules
│   ├── insert/              # Data‐cleaning & load scripts
│   └── visualize/           # Plotly‐based chart generators
│
└── static/
    ├── assets/              # Static image assets
    ├── css/                 # Stylesheets
    └── images/              #
```

---

## Deployment

We deploy to Google App Engine:

```bash
gcloud app deploy app.yaml --project="$GCLOUD_PROJECT"
```

Ensure your service-account has permissions for App Engine and Cloud Storage.

---

## Key Locations

- **Data ingestion**: `src/insert/*.py`  
- **Data fetching**: `src/fetch/*.py`  
- **Chart generation**: `src/visualize/*.py`  
- **Page layouts**: `pages/*.py`  
- **App entrypoint**: `app.py`

---

> **Note:** This README assumes Python 3.12, SQLite for local dev, and GCP for production.  
> Feel free to suggest corrections or updates!

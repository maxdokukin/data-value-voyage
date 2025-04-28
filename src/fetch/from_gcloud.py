# funcitons to fetch data from gcloud

import pandas as pd
from google.cloud import storage
from io import BytesIO

BUCKET_NAME = "value-voyage-cs163.appspot.com"

storage_client = storage.Client()

def load_csv_from_gcs(filename):
    """Load a single CSV file from GCS into a Pandas DataFrame."""
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    data = blob.download_as_bytes()
    df = pd.read_csv(BytesIO(data))
    return df

affordable_goods_df = load_csv_from_gcs("affordable_goods.csv")
analysis_df = load_csv_from_gcs("analysis.csv")
gamma_resampling_df = load_csv_from_gcs("gamma_resampling.csv")
gini_year_df = load_csv_from_gcs("gini_year.csv")
goods_prices_df = load_csv_from_gcs("goods_prices.csv")
incomes_df = load_csv_from_gcs("incomes.csv")
quintile_historical_df = load_csv_from_gcs("quintile_historical.csv")

def show_df_info(df, df_name="DataFrame"):
    """Prints basic info for a given DataFrame."""
    print(f"--- {df_name} ---")
    df.info()
    print("\n")
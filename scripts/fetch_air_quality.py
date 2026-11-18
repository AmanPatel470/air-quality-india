
import os
import time
import requests
import pandas as pd

from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# =====================================================
# 1. CONFIGURATION
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_DIR = os.path.join(
    BASE_DIR, "data", "clean"
)

COORDINATES_FILE = os.path.join(
    DATA_DIR, "district_coordinates.csv"
)

OUTPUT_FILE = os.path.join(
    DATA_DIR, "live_air_quality.csv"
)

TEMP_FILE = OUTPUT_FILE + ".tmp"

API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

POLLUTANTS = [
    "pm2_5",
    "pm10",
    "carbon_monoxide",
    "nitrogen_dioxide",
    "ozone"
]

COLUMN_MAPPING = {
    "pm2_5": "PM2.5",
    "pm10": "PM10",
    "carbon_monoxide": "CO",
    "nitrogen_dioxide": "NO2",
    "ozone": "O3"
}

POLLUTANT_COLUMNS = list(COLUMN_MAPPING.values())

# Multiple coordinates per API request
BATCH_SIZE = 10

# Delay between batches
REQUEST_DELAY = 5

# Refresh today and the previous two days
ROLLING_DAYS = 2

TIMEZONE = "Asia/Kolkata"


# =====================================================
# 2. REQUEST SESSION
# =====================================================

session = requests.Session()

retry_strategy = Retry(
    total=3,
    connect=3,
    read=3,
    status=0,
    backoff_factor=5,
    allowed_methods=["GET"]
)

adapter = HTTPAdapter(
    max_retries=retry_strategy
)

session.mount("https://", adapter)


# =====================================================
# 3. AQI CALCULATION
# =====================================================

def calculate_pm25_aqi(pm25):

    if pd.isna(pm25):
        return pd.NA

    value = max(0, float(pm25))

    breakpoints = [
        (0, 30, 0, 50),
        (31, 60, 51, 100),
        (61, 90, 101, 200),
        (91, 120, 201, 300),
        (121, 250, 301, 400),
        (251, 500, 401, 500)
    ]

    for c_low, c_high, i_low, i_high in breakpoints:

        if c_low <= value <= c_high:

            aqi = (
                (i_high - i_low)
                / (c_high - c_low)
            ) * (value - c_low) + i_low

            return round(aqi)

    return 500 if value > 500 else 0


def get_aqi_bucket(aqi):

    if pd.isna(aqi):
        return "Unknown"

    if aqi <= 50:
        return "Good"

    elif aqi <= 100:
        return "Satisfactory"

    elif aqi <= 200:
        return "Moderate"

    elif aqi <= 300:
        return "Poor"

    elif aqi <= 400:
        return "Very Poor"

    return "Severe"


# =====================================================
# 4. FETCH ONE BATCH OF DISTRICTS
# =====================================================

def fetch_batch(batch, today):

    latitudes = ",".join(
        str(float(row["Latitude"]))
        for _, row in batch.iterrows()
    )

    longitudes = ",".join(
        str(float(row["Longitude"]))
        for _, row in batch.iterrows()
    )

    params = {
        "latitude": latitudes,
        "longitude": longitudes,
        "hourly": ",".join(POLLUTANTS),
        "past_days": ROLLING_DAYS,
        "forecast_days": 1,
        "timezone": TIMEZONE,
        "domains": "cams_global"
    }

    for attempt in range(1, 6):

        try:

            response = session.get(
                API_URL,
                params=params,
                timeout=120
            )

            if response.status_code == 429:

                wait_time = min(
                    30 * attempt,
                    180
                )

                print(
                    f"Rate limited. Waiting {wait_time} seconds..."
                )

                time.sleep(wait_time)
                continue

            response.raise_for_status()

            response_data = response.json()

            if isinstance(response_data, dict):

                if response_data.get("error"):
                    raise ValueError(
                        response_data.get(
                            "reason",
                            "API returned an error"
                        )
                    )

                response_data = [response_data]

            if not isinstance(response_data, list):
                raise ValueError("Unexpected API response format.")

            if len(response_data) != len(batch):
                raise ValueError(
                    "API response count does not match batch size."
                )

            return response_data

        except (
            requests.exceptions.RequestException,
            ValueError
        ) as error:

            print(
                f"Attempt {attempt}/5 failed: {error}"
            )

            if attempt < 5:
                time.sleep(min(10 * attempt, 60))

    return None


# =====================================================
# 5. PROCESS ONE DISTRICT RESPONSE
# =====================================================

def process_district_response(
    state,
    district,
    response_data,
    today
):

    hourly = response_data.get("hourly")

    if not hourly or not hourly.get("time"):
        return None

    hourly_df = pd.DataFrame(hourly)

    hourly_df.rename(
        columns=COLUMN_MAPPING,
        inplace=True
    )

    for column in POLLUTANT_COLUMNS:

        if column not in hourly_df.columns:
            hourly_df[column] = pd.NA

        hourly_df[column] = pd.to_numeric(
            hourly_df[column],
            errors="coerce"
        )

    hourly_df["Date"] = pd.to_datetime(
        hourly_df["time"],
        errors="coerce"
    )

    hourly_df.dropna(
        subset=["Date"],
        inplace=True
    )

    hourly_df["Date"] = (
        hourly_df["Date"].dt.date
    )

    # Keep only today and the previous two days.
    start_date = today - timedelta(days=ROLLING_DAYS)

    hourly_df = hourly_df[
        (hourly_df["Date"] >= start_date)
        & (hourly_df["Date"] <= today)
    ].copy()

    if hourly_df.empty:
        return None

    daily_df = (
        hourly_df
        .groupby("Date", as_index=False)[POLLUTANT_COLUMNS]
        .mean()
    )

    daily_df["State"] = state
    daily_df["District"] = district

    daily_df["PM2.5_AQI"] = (
        daily_df["PM2.5"].apply(calculate_pm25_aqi)
    )

    daily_df["AQI_Bucket"] = (
        daily_df["PM2.5_AQI"].apply(get_aqi_bucket)
    )

    return daily_df[
        [
            "State",
            "District",
            "Date",
            "PM2.5",
            "PM10",
            "CO",
            "NO2",
            "O3",
            "PM2.5_AQI",
            "AQI_Bucket"
        ]
    ]


# =====================================================
# 6. LOAD EXISTING DATA
# =====================================================

def load_existing_data():

    if not os.path.exists(OUTPUT_FILE):

        return pd.DataFrame(
            columns=[
                "State",
                "District",
                "Date",
                "PM2.5",
                "PM10",
                "CO",
                "NO2",
                "O3",
                "PM2.5_AQI",
                "AQI_Bucket"
            ]
        )

    print("\nLoading existing historical dataset...")

    existing_df = pd.read_csv(OUTPUT_FILE)

    existing_df["Date"] = pd.to_datetime(
        existing_df["Date"],
        errors="coerce"
    ).dt.date

    return existing_df


# =====================================================
# 7. SAVE UPDATED DATA WITHOUT DUPLICATES
# =====================================================

def save_updated_data(existing_df, new_data):

    if new_data is None or new_data.empty:
        return existing_df

    updated_df = pd.concat(
        [existing_df, new_data],
        ignore_index=True
    )

    updated_df["Date"] = pd.to_datetime(
        updated_df["Date"],
        errors="coerce"
    ).dt.date

    # Replace old values for the same district and date.
    updated_df.drop_duplicates(
        subset=["State", "District", "Date"],
        keep="last",
        inplace=True
    )

    updated_df.sort_values(
        ["State", "District", "Date"],
        inplace=True
    )

    updated_df.reset_index(
        drop=True,
        inplace=True
    )

    updated_df.to_csv(
        TEMP_FILE,
        index=False
    )

    # Replace the original only after the temporary file is saved.
    os.replace(
        TEMP_FILE,
        OUTPUT_FILE
    )

    return updated_df


# =====================================================
# 8. MAIN AUTOMATIC DATA REFRESH
# =====================================================

def main():

    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )

    today = datetime.now().date()

    print("\n" + "=" * 60)
    print("       INDIA AIR QUALITY DATA REFRESH")
    print("=" * 60)

    print("Today's date:", today)
    print("Refreshing:", ROLLING_DAYS + 1, "days")
    print("Batch size:", BATCH_SIZE)

    if not os.path.exists(COORDINATES_FILE):

        print("\nERROR: District coordinates file not found.")
        print(COORDINATES_FILE)
        return

    districts_df = pd.read_csv(
        COORDINATES_FILE
    )

    required_columns = [
        "State",
        "District",
        "Latitude",
        "Longitude"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in districts_df.columns
    ]

    if missing_columns:

        print(
            "\nERROR: Missing columns:",
            missing_columns
        )
        return

    districts_df["Latitude"] = pd.to_numeric(
        districts_df["Latitude"],
        errors="coerce"
    )

    districts_df["Longitude"] = pd.to_numeric(
        districts_df["Longitude"],
        errors="coerce"
    )

    districts_df.dropna(
        subset=required_columns,
        inplace=True
    )

    districts_df = districts_df[
        districts_df["Latitude"].between(-90, 90)
        & districts_df["Longitude"].between(-180, 180)
    ].copy()

    districts_df.drop_duplicates(
        subset=["State", "District"],
        keep="first",
        inplace=True
    )

    districts_df.reset_index(
        drop=True,
        inplace=True
    )

    existing_df = load_existing_data()

    total = len(districts_df)

    print("\nTotal districts:", total)
    print("Existing historical rows:", len(existing_df))

    successful = 0
    failed = 0
    all_new_data = []

    batches = [
        districts_df.iloc[i:i + BATCH_SIZE]
        for i in range(0, total, BATCH_SIZE)
    ]

    print("Total API batches:", len(batches))
    print("\nStarting refresh...\n")

    for batch_number, batch in enumerate(
        batches,
        start=1
    ):

        print(
            f"[BATCH {batch_number}/{len(batches)}] "
            f"Fetching {len(batch)} districts..."
        )

        response_list = fetch_batch(
            batch,
            today
        )

        if response_list is None:

            failed += len(batch)

            print("Batch failed. Existing data preserved.")

        else:

            batch_data = []

            for index, (_, row) in enumerate(
                batch.iterrows()
            ):

                state = str(row["State"])
                district = str(row["District"])

                district_data = process_district_response(
                    state,
                    district,
                    response_list[index],
                    today
                )

                if (
                    district_data is not None
                    and not district_data.empty
                ):

                    batch_data.append(district_data)
                    successful += 1

                else:

                    failed += 1

                    print(
                        f"  No usable data: {state} - {district}"
                    )

            if batch_data:

                combined_batch = pd.concat(
                    batch_data,
                    ignore_index=True
                )

                existing_df = save_updated_data(
                    existing_df,
                    combined_batch
                )

                print(
                    f"  Saved {len(combined_batch)} daily records."
                )

        if batch_number < len(batches):
            time.sleep(REQUEST_DELAY)

    # =================================================
    # 9. FINAL REPORT
    # =================================================

    print("\n" + "=" * 60)
    print("             REFRESH COMPLETED")
    print("=" * 60)

    print("Successful districts:", successful)
    print("Failed districts:", failed)

    if not existing_df.empty:

        print(
            "Total records:",
            len(existing_df)
        )

        print(
            "Unique districts:",
            existing_df[
                ["State", "District"]
            ].drop_duplicates().shape[0]
        )

        print(
            "Unique states:",
            existing_df["State"].nunique()
        )

        print(
            "Latest available date:",
            existing_df["Date"].max()
        )

        print(
            "Date range:",
            existing_df["Date"].min(),
            "to",
            existing_df["Date"].max()
        )

    print("\nUpdated file:")
    print(OUTPUT_FILE)

    print("=" * 60)


if __name__ == "__main__":
    main()

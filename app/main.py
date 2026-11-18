import os
import html
import base64
import plotly.graph_objects as go

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AQI Forecast",
    layout="wide"
)


# =====================================================
# 2. MINECRAFT THEME
# =====================================================

custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

:root {
    --mc-bg: #121212;
    --mc-sidebar: #1e1e1e;
    --mc-cyan: #00ffcc;
    --mc-pink: #ff0055;
    --mc-teal: #245b55;
}

.stApp {
    background-color: var(--mc-bg) !important;
    color: #e0e0e0;
    font-family: 'VT323', monospace !important;
}

h1, h2, h3 {
    font-family: 'VT323', monospace !important;
    color: var(--mc-cyan) !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    text-shadow: 2px 2px var(--mc-pink);
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background-color: var(--mc-sidebar) !important;
    border-right: 2px solid var(--mc-cyan);
}

[data-testid="stSidebar"] label {
    color: var(--mc-cyan) !important;
    font-family: 'VT323', monospace !important;
    font-size: 22px !important;
}

/* CLOSED DROPDOWNS */

[data-testid="stSidebar"] [data-baseweb="select"] {
    background-color: var(--mc-bg) !important;
    border-radius: 0 !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: var(--mc-bg) !important;
    background-color: var(--mc-bg) !important;
    border: 2px solid var(--mc-cyan) !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    min-height: 48px !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div > div {
    background: transparent !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-baseweb="select"] div,
[data-testid="stSidebar"] [data-baseweb="select"] input {
    font-family: 'VT323', monospace !important;
    color: var(--mc-cyan) !important;
    font-size: 19px !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] input {
    background: transparent !important;
    caret-color: var(--mc-cyan) !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] input::placeholder {
    color: #777777 !important;
    opacity: 1 !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] svg {
    fill: var(--mc-cyan) !important;
    color: var(--mc-cyan) !important;
}

/* OPEN DROPDOWN */

[data-baseweb="popover"],
[data-baseweb="popover"] > div,
[data-baseweb="menu"],
[data-baseweb="popover"] ul {
    background-color: var(--mc-sidebar) !important;
    border-radius: 0 !important;
}

[data-baseweb="popover"] {
    border: 2px solid var(--mc-cyan) !important;
    box-shadow: 4px 4px 0 #080808 !important;
}

[data-baseweb="popover"] li,
[data-baseweb="popover"] [role="option"],
[role="listbox"] [role="option"] {
    background-color: var(--mc-sidebar) !important;
    color: var(--mc-cyan) !important;
    font-family: 'VT323', monospace !important;
    font-size: 21px !important;
}

[data-baseweb="popover"] li:hover,
[data-baseweb="popover"] [role="option"]:hover,
[role="listbox"] [role="option"]:hover {
    background-color: var(--mc-teal) !important;
    color: #ffffff !important;
}

[data-baseweb="popover"] [aria-selected="true"],
[role="listbox"] [aria-selected="true"] {
    background-color: var(--mc-teal) !important;
    color: var(--mc-cyan) !important;
}

[data-baseweb="popover"] input {
    background-color: var(--mc-bg) !important;
    color: var(--mc-cyan) !important;
    border: 2px solid var(--mc-cyan) !important;
    border-radius: 0 !important;
    font-family: 'VT323', monospace !important;
    font-size: 20px !important;
}

/* DROPDOWN SCROLLBAR */

[data-baseweb="popover"] ::-webkit-scrollbar {
    width: 8px;
}

[data-baseweb="popover"] ::-webkit-scrollbar-track {
    background: var(--mc-bg);
}

[data-baseweb="popover"] ::-webkit-scrollbar-thumb {
    background: var(--mc-cyan);
}

/* BUTTONS */

.stButton > button {
    background-color: var(--mc-sidebar) !important;
    color: var(--mc-cyan) !important;
    border: 2px solid var(--mc-cyan) !important;
    border-radius: 0 !important;
    font-family: 'VT323', monospace !important;
    font-size: 22px !important;
}

.stButton > button:hover {
    background-color: var(--mc-cyan) !important;
    color: var(--mc-bg) !important;
    border-color: var(--mc-pink) !important;
}

/* METRICS */

[data-testid="stMetricValue"] {
    font-family: 'VT323', monospace !important;
    font-size: 3rem !important;
    color: var(--mc-pink) !important;
    text-shadow: 1px 1px var(--mc-cyan);
}

[data-testid="stMetricLabel"] {
    font-family: 'VT323', monospace !important;
    font-size: 1.5rem !important;
    color: #a0a0a0 !important;
}

[data-testid="stSidebar"] button {
    font-size: 14px !important;
    white-space: nowrap !important;
    padding: 8px 4px !important;
}

[data-testid="stSidebar"] button p {
    font-size: 14px !important;
    white-space: nowrap !important;
}

/* Reduce spacing around AQI MAP and location icon */
div.st-key-india_map_button {
    margin-bottom: -20px !important;
}

[data-testid="stSidebar"] [data-testid="stImage"] {
    margin-top: -10px !important;
}


/* ALERTS */

.stAlert {
    border-radius: 0 !important;
    border: 2px solid var(--mc-cyan) !important;
    background-color: var(--mc-bg) !important;
    color: #e0e0e0 !important;
    font-family: 'VT323', monospace !important;
}

</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)


# =====================================================
# 3. APPLICATION TITLE
# =====================================================

st.title("INDIA AIR QUALITY TERMINAL")

st.write(
    "District-level air quality monitoring and next-day forecasting system."
)


# =====================================================
# 4. LOAD DATA
# =====================================================

@st.cache_data
def load_live_data(file_modified):

    base_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    file_path = os.path.join(
        base_dir,
        "data",
        "clean",
        "live_air_quality.csv"
    )

    data = pd.read_csv(file_path)

    required_columns = [
        "State",
        "District",
        "Date",
        "PM2.5",
        "PM10",
        "CO",
        "NO2",
        "O3",
        "PM2.5_AQI"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing dataset columns: {missing_columns}"
        )

    data["Date"] = pd.to_datetime(
        data["Date"],
        errors="coerce"
    )

    numeric_columns = [
        "PM2.5",
        "PM10",
        "CO",
        "NO2",
        "O3",
        "PM2.5_AQI"
    ]

    for column in numeric_columns:
        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

    data.dropna(
        subset=required_columns,
        inplace=True
    )

    data.drop_duplicates(
        subset=["State", "District", "Date"],
        keep="last",
        inplace=True
    )

    data.sort_values(
        ["State", "District", "Date"],
        inplace=True
    )

    return data


# Get the CSV modification time.
# When the dataset changes, Streamlit reloads it.

base_dir = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

data_path = os.path.join(
    base_dir,
    "data",
    "clean",
    "live_air_quality.csv"
)

try:
    df = load_live_data(os.path.getmtime(data_path))

except Exception as error:
    st.error(f"Unable to load dataset: {error}")
    st.stop()


# =====================================================
# 5. AQI FUNCTIONS
# =====================================================

def calc_aqi(pm25):

    if pd.isna(pm25):
        return None

    pm25 = max(0, float(pm25))

    breakpoints = [
        (0, 30, 0, 50),
        (30, 60, 50, 100),
        (60, 90, 100, 200),
        (90, 120, 200, 300),
        (120, 250, 300, 400),
        (250, 500, 400, 500)
    ]

    for c_low, c_high, i_low, i_high in breakpoints:

        if c_low <= pm25 < c_high:

            value = (
                (i_high - i_low) /
                (c_high - c_low)
            ) * (pm25 - c_low) + i_low

            return round(value)

    return 500


def get_aqi_color(aqi):

    if aqi <= 50:
        return "#00C853"
    elif aqi <= 100:
        return "#A8D900"
    elif aqi <= 200:
        return "#FFD600"
    elif aqi <= 300:
        return "#FF8C00"
    elif aqi <= 400:
        return "#D50000"

    return "#7B0000"


def get_aqi_text_color(aqi):
    return "#FFFFFF" if aqi > 300 else "#121212"


def get_aqi_status(aqi):

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
# 6. MARQUEE
# =====================================================



def show_marquee(message):

    safe_message = html.escape(message)

    marquee_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
* {{
    box-sizing: border-box;
}}

html, body {{
    margin: 0;
    padding: 0;
    width: 100%;
    background: transparent;
    overflow: hidden;
}}

.marquee-box {{
    width: 100%;
    height: 75px;
    overflow: hidden;
    white-space: nowrap;
    background: #121212;
    border: 2px solid #00ffcc;
    display: flex;
    align-items: center;
}}

.marquee-track {{
    display: flex;
    width: max-content;
    flex-shrink: 0;
    animation: scroll-left 25s linear infinite;
    will-change: transform;
}}

.marquee-group {{
    display: flex;
    flex-shrink: 0;
    align-items: center;
    white-space: nowrap;
}}

.marquee-group span {{
    display: block;
    flex-shrink: 0;
    padding-right: 100px;
    color: #00ffcc;
    font-family: monospace;
    font-size: 23px;
    font-weight: bold;
    white-space: nowrap;
}}

.marquee-box:hover .marquee-track {{
    animation-play-state: paused;
}}

@keyframes scroll-left {{
    0% {{
        transform: translateX(0);
    }}
    100% {{
        transform: translateX(-50%);
    }}
}}
</style>
</head>

<body>

<div class="marquee-box">

    <div class="marquee-track">

        <div class="marquee-group">
            <span>{safe_message}</span>
        </div>

        <div class="marquee-group">
            <span>{safe_message}</span>
        </div>

    </div>

</div>

</body>
</html>
"""

    components.html(
        marquee_html,
        height=80,
        scrolling=False
    )




# =====================================================
# 7. AQI CARD
# =====================================================

def show_aqi_card(container, title, aqi, status):

    background = get_aqi_color(aqi)
    foreground = get_aqi_text_color(aqi)

    card_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
@import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

* {{
    box-sizing: border-box;
}}

html, body {{
    margin: 0;
    padding: 0;
    background: transparent;
    overflow: hidden;
}}

.aqi-card {{
    width: 100%;
    height: 170px;
    padding: 15px 5px;
    background: {background};
    color: {foreground};
    text-align: center;
    border: 3px solid #252525;
    box-shadow: 4px 4px 0 #080808;
    font-family: 'VT323', monospace;
}}

.aqi-label {{
    font-size: 20px;
}}

.aqi-value {{
    font-size: 48px;
    font-weight: bold;
    margin: 5px 0;
}}

.aqi-status {{
    font-size: 22px;
}}
</style>
</head>

<body>

<div class="aqi-card">
    <div class="aqi-label">
        {html.escape(title)}
    </div>

    <div class="aqi-value">
        {aqi}
    </div>

    <div class="aqi-status">
        {html.escape(status.upper())}
    </div>
</div>

</body>
</html>
"""

    with container:
        components.html(
            card_html,
            height=185,
            scrolling=False
        )


# =====================================================
# 8. SESSION STATE CALLBACKS
# =====================================================

def on_state_change():
    st.session_state["selected_district"] = None


def clear_selection():
    st.session_state["selected_state"] = None
    st.session_state["selected_district"] = None


# =====================================================
# 9. SIDEBAR - SEARCHABLE DROPDOWNS
# =====================================================

st.sidebar.header("> SELECT REGION")

states = sorted(
    df["State"].dropna().unique().tolist()
)

state = st.sidebar.selectbox(
    "SEARCH STATE / UNION TERRITORY",
    options=states,
    index=None,
    placeholder="Select state...",
    key="selected_state",
    on_change=on_state_change
)

if state is not None:

    districts = sorted(
        df.loc[
            df["State"] == state,
            "District"
        ].dropna().unique().tolist()
    )

else:
    districts = []

district = st.sidebar.selectbox(
    "SEARCH DISTRICT",
    options=districts,
    index=None,
    placeholder="Select district...",
    key="selected_district",
    disabled=(state is None)
)

st.sidebar.markdown("---")

st.markdown("""
<style>
/* AQI MAP text button */
div.st-key-india_map_button button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    justify-content: flex-start !important;
}

div.st-key-india_map_button button p {
    color: #00ffcc !important;
    font-family: monospace !important;
    font-size: 21px !important;
    font-weight: bold !important;
    text-shadow: 2px 0 #ff0055 !important;
    white-space: nowrap !important;
}

div.st-key-india_map_button button:hover {
    background: transparent !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)



st.sidebar.markdown("""
<style>

/* Smaller image with continuous floating animation */
[data-testid="stSidebar"] [data-testid="stImage"] img {
    width: 60px !important;
    transition: transform 0.3s ease-in-out;
    animation: floatLocation 2.5s ease-in-out infinite;
    transform-origin: center;
}

/* Floating movement */
@keyframes floatLocation {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-10px);
    }
}

/* Hover enlargement */
[data-testid="stSidebar"] [data-testid="stImage"] img:hover {
    transform: scale(1.2);
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)





# =====================================================
# 11. CLEAR SELECTION
# =====================================================

if state is not None or district is not None:

    st.sidebar.button(
        "[ CLEAR SELECTION ]",
        key="clear_selection_button",
        use_container_width=True,
        on_click=clear_selection
    )



# =====================================================
# 12. HOMEPAGE - INDIA AQI MAP + TOP 5 HIGHEST AQI
# =====================================================

if state is None and district is None:

    latest_districts = (
        df.sort_values("Date")
        .groupby(["State", "District"])
        .tail(1)
        .copy()
    )

    latest_districts.dropna(
        subset=["PM2.5_AQI"],
        inplace=True
    )

    top_5 = (
        latest_districts
        .sort_values("PM2.5_AQI", ascending=False)
        .head(5)
    )

    report_date = latest_districts["Date"].max()

    # -------------------------------------------------
    # FIRST MARQUEE
    # -------------------------------------------------

    st.markdown("---")

    show_marquee(
        "SEARCH AND SELECT A STATE OR DISTRICT "
        "FROM THE SIDEBAR TO VIEW ITS AIR QUALITY DASHBOARD."
    )

    # -------------------------------------------------
    # INDIA AQI MAP
    # -------------------------------------------------

    st.markdown("---")
    st.title("INDIA AIR QUALITY MAP")

    coordinates_path = os.path.join(
        base_dir,
        "data",
        "clean",
        "district_coordinates.csv"
    )

    try:

        coordinates = pd.read_csv(coordinates_path)

        # Prepare latest AQI records
        latest_map_data = latest_districts.copy()

        latest_map_data["State"] = (
            latest_map_data["State"].astype(str).str.strip()
        )

        latest_map_data["match_key"] = (
            latest_map_data["District"]
            .astype(str)
            .str.lower()
            .str.replace(r"[^a-z0-9]", "", regex=True)
        )

        # Prepare coordinate matching using both
        # District and Boundary District columns
        coordinate_matches = []

        for column in ["District", "Boundary District"]:

            if column in coordinates.columns:

                temp = coordinates[
                    ["State", column, "Latitude", "Longitude"]
                ].copy()

                temp.rename(
                    columns={column: "District"},
                    inplace=True
                )

                temp["State"] = (
                    temp["State"].astype(str).str.strip()
                )

                temp["match_key"] = (
                    temp["District"]
                    .astype(str)
                    .str.lower()
                    .str.replace(r"[^a-z0-9]", "", regex=True)
                )

                coordinate_matches.append(temp)

        coordinate_data = pd.concat(
            coordinate_matches,
            ignore_index=True
        )

        coordinate_data.drop_duplicates(
            subset=["State", "match_key"],
            inplace=True
        )

        # Convert coordinates to numeric
        coordinate_data["Latitude"] = pd.to_numeric(
            coordinate_data["Latitude"],
            errors="coerce"
        )

        coordinate_data["Longitude"] = pd.to_numeric(
            coordinate_data["Longitude"],
            errors="coerce"
        )

        # Match AQI records with district coordinates
        map_data = latest_map_data.merge(
            coordinate_data[
                ["State", "match_key", "Latitude", "Longitude"]
            ],
            on=["State", "match_key"],
            how="inner"
        )

        map_data.dropna(
            subset=[
                "Latitude",
                "Longitude",
                "PM2.5_AQI"
            ],
            inplace=True
        )

        if not map_data.empty:

            fig_map = go.Figure()

            fig_map.add_trace(
                go.Scattergeo(
                    lat=map_data["Latitude"],
                    lon=map_data["Longitude"],
                    text=map_data["District"],

                    customdata=map_data[
                        ["State", "PM2.5_AQI", "Date"]
                    ].to_numpy(),

                    mode="markers",

                    marker=dict(
                        size=9,
                        color=map_data["PM2.5_AQI"],
                        colorscale=[
                            [0.0, "#00C853"],
                            [0.1, "#A8D900"],
                            [0.3, "#FFD600"],
                            [0.5, "#FF8C00"],
                            [0.7, "#D50000"],
                            [1.0, "#7B0000"]
                        ],
                        cmin=0,
                        cmax=500,
                        opacity=0.9,
                        line=dict(
                            color="#00ffcc",
                            width=0.5
                        ),
                        colorbar=dict(
                            title="AQI",
                            tickfont=dict(color="#00ffcc")
                        )
                    ),

                    hovertemplate=(
                        "<b>%{text}</b><br>"
                        "State: %{customdata[0]}<br>"
                        "PM2.5 AQI: %{customdata[1]:.0f}<br>"
                        "Date: %{customdata[2]|%d/%m/%Y}"
                        "<extra></extra>"
                    )
                )
            )

            fig_map.update_layout(
                height=650,
                paper_bgcolor="#121212",
                plot_bgcolor="#121212",

                font=dict(
                    family="VT323, monospace",
                    color="#00ffcc",
                    size=16
                ),

                geo=dict(
                    scope="asia",
                    projection_type="mercator",
                    showland=True,
                    landcolor="#1e1e1e",
                    showcountries=True,
                    countrycolor="#00ffcc",
                    showocean=True,
                    oceancolor="#121212",
                    bgcolor="#121212",
                    lonaxis=dict(range=[67, 99]),
                    lataxis=dict(range=[5, 38])
                ),

                margin=dict(
                    l=0,
                    r=0,
                    t=20,
                    b=0
                )
            )

            st.plotly_chart(
                fig_map,
                use_container_width=True,
                config={"displayModeBar": True}
            )

            st.caption(
                f"MAP DATA: {len(map_data)} MATCHED DISTRICTS | "
                "COLOURS REPRESENT PM2.5 AQI ESTIMATES."
            )

        else:

            st.warning(
                "No matching district coordinates were found."
            )

    except FileNotFoundError:

        st.error(
            "district_coordinates.csv not found in data/clean."
        )

    except Exception as error:

        st.error(
            f"India AQI map error: {error}"
        )

    # -------------------------------------------------
    # TOP 5 LEADERBOARD
    # -------------------------------------------------

    st.markdown("---")

    st.title("TOP 5 HIGHEST AQI DISTRICTS")

    st.subheader(
        f"ON {report_date.strftime('%d/%m/%Y')}"
    )

    st.caption(
        "INDIA AIR QUALITY LEADERBOARD // "
        "RANKED BY LATEST AVAILABLE PM2.5 AQI SUB-INDEX"
    )

    table_rows = ""

    for rank, (_, row) in enumerate(
        top_5.iterrows(),
        start=1
    ):

        aqi_value = int(round(row["PM2.5_AQI"]))
        aqi_color = get_aqi_color(aqi_value)

        state_name = html.escape(str(row["State"]))
        district_name = html.escape(str(row["District"]))

        table_rows += f"""
        <tr>
            <td class="rank-cell">#{rank:02d}</td>
            <td>{state_name}</td>
            <td>{district_name}</td>
            <td class="aqi-cell">
                <span style="color:{aqi_color};">
                    {aqi_value}
                </span>
            </td>
        </tr>
        """

    leaderboard_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    padding: 4px;
    background: transparent;
}}

.mc-table-wrap {{
    width: 100%;
    border: 4px solid #697575;
    border-right-color: #252d2d;
    border-bottom-color: #252d2d;
    background: #202727;
    box-shadow: 5px 5px 0 #080b0b;
}}

.mc-table {{
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
    font-family: monospace;
    font-size: 17px;
    color: #f0f5f3;
}}

.mc-table th {{
    background: #245b55;
    color: #d9fff5;
    text-align: left;
    padding: 14px 16px;
    border: 2px solid #152f2c;
    border-bottom: 4px solid #102522;
    letter-spacing: 1px;
}}

.mc-table td {{
    background: #293333;
    padding: 14px 16px;
    border: 2px solid #151d1d;
    overflow-wrap: anywhere;
}}

.mc-table tr:nth-child(even) td {{
    background: #374343;
}}

.mc-table .rank-cell {{
    text-align: center;
    color: #00ffcc;
}}

.mc-table .aqi-cell {{
    text-align: center;
    font-size: 22px;
    font-weight: bold;
}}
</style>
</head>

<body>

<div class="mc-table-wrap">
<table class="mc-table">

<thead>
<tr>
    <th style="width:12%;">RANK</th>
    <th style="width:27%;">STATE</th>
    <th style="width:36%;">DISTRICT</th>
    <th style="width:25%;text-align:center;">AQI</th>
</tr>
</thead>

<tbody>
{table_rows}
</tbody>

</table>
</div>

</body>
</html>
"""

    components.html(
        leaderboard_html,
        height=330,
        scrolling=False
    )

    # -------------------------------------------------
    # AQI COLOUR LEGEND
    # -------------------------------------------------

    st.markdown("### AQI COLOUR LEGEND")

    legend_html = """
<!DOCTYPE html>
<html>
<head>
<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 4px;
    background: transparent;
    font-family: monospace;
}

.legend {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.legend-item {
    padding: 7px 10px;
    border: 2px solid #101515;
    box-shadow: 2px 2px 0 #080b0b;
    font-size: 13px;
    font-weight: bold;
}
</style>
</head>

<body>

<div class="legend">

    <div class="legend-item"
         style="background:#00C853;color:#121212;">
        GOOD [0-50]
    </div>

    <div class="legend-item"
         style="background:#A8D900;color:#121212;">
        SATISFACTORY [51-100]
    </div>

    <div class="legend-item"
         style="background:#FFD600;color:#121212;">
        MODERATE [101-200]
    </div>

    <div class="legend-item"
         style="background:#FF8C00;color:#121212;">
        POOR [201-300]
    </div>

    <div class="legend-item"
         style="background:#D50000;color:#FFFFFF;">
        VERY POOR [301-400]
    </div>

    <div class="legend-item"
         style="background:#7B0000;color:#FFFFFF;">
        SEVERE [401-500]
    </div>

</div>
</body>
</html>
"""

    components.html(
        legend_html,
        height=90,
        scrolling=False
    )

    st.caption(
        "AQI values are PM2.5-based sub-index estimates, "
        "not complete official CPCB AQI readings."
    )

    st.stop()



    # =================================================
    # 13. AQI COLOUR LEGEND
    # =================================================

    st.markdown("### AQI COLOUR LEGEND")

    legend_html = """
<!DOCTYPE html>
<html>
<head>
<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 4px;
    background: transparent;
    font-family: monospace;
}

.legend {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.legend-item {
    padding: 7px 10px;
    border: 2px solid #101515;
    box-shadow: 2px 2px 0 #080b0b;
    font-size: 13px;
    font-weight: bold;
}
</style>
</head>

<body>

<div class="legend">

    <div class="legend-item"
         style="background:#00C853;color:#121212;">
        GOOD [0-50]
    </div>

    <div class="legend-item"
         style="background:#A8D900;color:#121212;">
        SATISFACTORY [51-100]
    </div>

    <div class="legend-item"
         style="background:#FFD600;color:#121212;">
        MODERATE [101-200]
    </div>

    <div class="legend-item"
         style="background:#FF8C00;color:#121212;">
        POOR [201-300]
    </div>

    <div class="legend-item"
         style="background:#D50000;color:#FFFFFF;">
        VERY POOR [301-400]
    </div>

    <div class="legend-item"
         style="background:#7B0000;color:#FFFFFF;">
        SEVERE [401-500]
    </div>

</div>
</body>
</html>
"""

    components.html(
        legend_html,
        height=90,
        scrolling=False
    )

    st.caption(
        "AQI values are PM2.5-based sub-index estimates, "
        "not complete official CPCB AQI readings."
    )

    st.stop()


# =====================================================
# 14. STATE SELECTED, DISTRICT NOT SELECTED
# =====================================================

if state is not None and district is None:

    st.markdown("---")

    st.subheader(
        f"STATE SELECTED: {state.upper()}"
    )

    show_marquee(
        "SEARCH AND SELECT A DISTRICT "
        "TO VIEW ITS AIR QUALITY DASHBOARD."
    )


# =====================================================
# 15. SELECTED DISTRICT DATA
# =====================================================

district_data = df[
    (df["State"] == state) &
    (df["District"] == district)
].copy()

district_data.sort_values(
    "Date",
    inplace=True
)

district_data.reset_index(
    drop=True,
    inplace=True
)

if len(district_data) < 30:
    st.stop()

latest_data = district_data.iloc[-1]


# =====================================================
# 16. CURRENT AIR QUALITY
# =====================================================

current_aqi = calc_aqi(latest_data["PM2.5"])
current_status = get_aqi_status(current_aqi)

st.subheader(
    f"DATA: {district}, {state} // "
    f"{latest_data['Date'].strftime('%d/%m/%Y')}"
)


# =====================================================
# 17. POLLUTANT METRICS
# =====================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "PM2.5",
    f"{latest_data['PM2.5']:.1f} µg/m³"
)

col2.metric(
    "PM10",
    f"{latest_data['PM10']:.1f} µg/m³"
)

col3.metric(
    "NO2",
    f"{latest_data['NO2']:.1f}"
)

show_aqi_card(
    col4,
    "PM2.5 AQI SUB-INDEX",
    current_aqi,
    current_status
)

st.write(
    f"AIR QUALITY STATUS: {current_status.upper()}"
)

st.caption(
    "AQI shown here is a PM2.5-based sub-index estimate, "
    "not the complete official CPCB AQI."
)


# =====================================================
# 18. NEXT-DAY AIR QUALITY FORECAST
# =====================================================

st.markdown("---")

st.subheader("NEXT-DAY AIR QUALITY FORECAST")

features = [
    "PM2.5",
    "PM2.5_Lag7",
    "PM10",
    "NO2",
    "CO",
    "O3"
]

ml_data = district_data.copy()

ml_data["PM2.5_Lag7"] = (
    ml_data["PM2.5"].shift(7)
)

ml_data["Target_PM2.5"] = (
    ml_data["PM2.5"].shift(-1)
)

ml_data.dropna(
    subset=features + ["Target_PM2.5"],
    inplace=True
)

if len(ml_data) < 50:
    st.error(
        "Not enough historical records for model evaluation."
    )
    st.stop()


# =====================================================
# 19. CHRONOLOGICAL MODEL EVALUATION
# =====================================================

X = ml_data[features]
y = ml_data["Target_PM2.5"]

split_index = int(len(ml_data) * 0.80)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

evaluation_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

evaluation_model.fit(X_train, y_train)

test_predictions = evaluation_model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    test_predictions
)

r2 = r2_score(
    y_test,
    test_predictions
)


# =====================================================
# 20. FINAL MODEL TRAINING
# =====================================================

model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(X, y)


# =====================================================
# 21. MODEL PERFORMANCE
# =====================================================

st.markdown("### MODEL PERFORMANCE")

metric1, metric2 = st.columns(2)

metric1.metric(
    "MAE",
    f"{mae:.2f} µg/m³"
)

metric2.metric(
    "R² SCORE",
    f"{r2:.3f}"
)

st.caption(
    "Evaluation uses an earlier 80% training period and "
    "the latest 20% testing period. Metrics are specific "
    "to the selected district."
)


# =====================================================
# 22. NEXT-DAY PREDICTION
# =====================================================

if len(district_data) < 8:

    st.error(
        "Not enough observations for the seven-day lag."
    )

else:

    latest_pm25 = latest_data["PM2.5"]
    lag7_pm25 = district_data["PM2.5"].iloc[-8]

    input_data = pd.DataFrame(
        [[
            latest_pm25,
            lag7_pm25,
            latest_data["PM10"],
            latest_data["NO2"],
            latest_data["CO"],
            latest_data["O3"]
        ]],
        columns=features
    )

    if st.button("[ RUN NEXT-DAY PREDICTION ]"):

        predicted_pm25 = float(
            model.predict(input_data)[0]
        )

        predicted_pm25 = max(
            0,
            predicted_pm25
        )

        predicted_aqi = calc_aqi(predicted_pm25)
        predicted_status = get_aqi_status(predicted_aqi)

        forecast_date = (
            latest_data["Date"] +
            pd.Timedelta(days=1)
        )

        # HEALTH ADVICE

        if predicted_aqi <= 100:
            advice = "Monitor air quality."
        elif predicted_aqi <= 200:
            advice = "Sensitive groups should take care."
        elif predicted_aqi <= 300:
            advice = "Reduce prolonged outdoor exposure."
        elif predicted_aqi <= 400:
            advice = "Avoid prolonged outdoor exposure."
        else:
            advice = "Avoid outdoor exposure."

        # =============================================
        # FORECAST MESSAGE
        # IMPORTANT: components.html RENDERS THE HTML
        # =============================================

        forecast_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
@import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

* {{
    box-sizing: border-box;
}}

html, body {{
    margin: 0;
    padding: 0;
    background: transparent;
    overflow: hidden;
}}

.forecast {{
    width: 100%;
    background: #121212;
    color: #00ffcc;
    border: 2px solid #00ffcc;
    padding: 12px 16px;
    font-family: 'VT323', monospace;
    font-size: 25px;
    line-height: 1.6;
    letter-spacing: 1px;
}}

.forecast-line {{
    color: #00ffcc;
    text-shadow: 1px 1px #ff0055;
}}

</style>
</head>

<body>

<div class="forecast">

    <div class="forecast-line">
        &gt;FORECAST DATE: {forecast_date.strftime('%d/%m/%Y')}
    </div>

    <div class="forecast-line">
        &gt;{html.escape(predicted_status.upper())}: {html.escape(advice)}
    </div>

</div>

</body>
</html>
"""

        # Render actual HTML in its own component
        components.html(
            forecast_html,
            height=100,
            scrolling=False
        )

        st.markdown("---")

        # PREDICTED VALUES

        result1, result2 = st.columns(2)

        result1.metric(
            "PREDICTED PM2.5",
            f"{predicted_pm25:.2f} µg/m³"
        )

        show_aqi_card(
            result2,
            "PREDICTED PM2.5 AQI",
            predicted_aqi,
            predicted_status
        )

# =====================================================
# 23. MINECRAFT-STYLE POLLUTION ANALYTICS
# =====================================================

st.markdown("---")

st.title("POLLUTION ANALYTICS TERMINAL")


# -----------------------------------------------------
# REUSABLE DARK CHART DESIGN
# -----------------------------------------------------

def style_chart(fig, height=380):

    fig.update_layout(
        height=height,

        paper_bgcolor="#121212",
        plot_bgcolor="#1e1e1e",

        font=dict(
            family="VT323, monospace",
            size=17,
            color="#00ffcc"
        ),

        title_font=dict(
            family="VT323, monospace",
            size=25,
            color="#00ffcc"
        ),

        legend=dict(
            bgcolor="#121212",
            bordercolor="#00ffcc",
            borderwidth=1,
            font=dict(
                family="VT323, monospace",
                size=16,
                color="#00ffcc"
            )
        ),

        margin=dict(
            l=45,
            r=25,
            t=65,
            b=45
        ),

        hoverlabel=dict(
            bgcolor="#121212",
            bordercolor="#00ffcc",
            font=dict(
                family="VT323, monospace",
                size=17,
                color="#00ffcc"
            )
        ),

        xaxis=dict(
            showgrid=False,
            showline=True,
            linecolor="#00ffcc",
            tickfont=dict(color="#00ffcc"),
            title_font=dict(color="#ff0055")
        ),

        yaxis=dict(
            showgrid=True,
            gridcolor="#245b55",
            gridwidth=1,
            zeroline=False,
            showline=True,
            linecolor="#00ffcc",
            tickfont=dict(color="#00ffcc"),
            title_font=dict(color="#ff0055")
        )
    )

    return fig


# -----------------------------------------------------
# A. HISTORICAL PM2.5 AND PM10
# -----------------------------------------------------

st.subheader("> 90-DAY POLLUTION HISTORY")

historical_data = district_data.tail(90).copy()

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=historical_data["Date"],
        y=historical_data["PM2.5"],
        name="PM2.5",
        mode="lines",
        line=dict(
            color="#00ffcc",
            width=3
        ),
        fill="tozeroy",
        fillcolor="rgba(0,255,204,0.06)"
    )
)

fig.add_trace(
    go.Scatter(
        x=historical_data["Date"],
        y=historical_data["PM10"],
        name="PM10",
        mode="lines",
        line=dict(
            color="#ff0055",
            width=3
        )
    )
)

fig.update_layout(
    title="PM2.5 VS PM10 CONCENTRATION",
    xaxis_title="DATE",
    yaxis_title="CONCENTRATION (µg/m³)",
    hovermode="x unified"
)

st.plotly_chart(
    style_chart(fig),
    use_container_width=True,
    config={"displayModeBar": True}
)


# -----------------------------------------------------
# B. POLLUTANT COMPARISON
# -----------------------------------------------------

st.markdown("---")

st.subheader("> POLLUTANT COMPARISON")

pollutants = [
    "PM2.5",
    "PM10",
    "CO",
    "NO2",
    "O3"
]

comparison_data = (
    historical_data
    .set_index("Date")[pollutants]
)

max_values = comparison_data.max().replace(0, 1)

normalized_data = (
    comparison_data
    .div(max_values)
    .mul(100)
)

pollutant_colors = {
    "PM2.5": "#00ffcc",
    "PM10": "#ff0055",
    "CO": "#ffd600",
    "NO2": "#00aaff",
    "O3": "#a855f7"
}

fig = go.Figure()

for pollutant in pollutants:

    fig.add_trace(
        go.Scatter(
            x=normalized_data.index,
            y=normalized_data[pollutant],
            name=pollutant,
            mode="lines",
            line=dict(
                color=pollutant_colors[pollutant],
                width=2
            )
        )
    )

fig.update_layout(
    title="NORMALIZED POLLUTANT ACTIVITY",
    xaxis_title="DATE",
    yaxis_title="RELATIVE LEVEL (%)",
    hovermode="x unified"
)

st.plotly_chart(
    style_chart(fig),
    use_container_width=True
)

st.caption(
    "Values are normalized against each pollutant's "
    "maximum over the selected 90-day period. "
    "This compares relative variation, not absolute concentration."
)


# -----------------------------------------------------
# C. MONTHLY POLLUTION PATTERN
# -----------------------------------------------------

st.markdown("---")

st.subheader("> MONTHLY POLLUTION ANALYSIS")

monthly_data = district_data.copy()

monthly_data["Month"] = (
    monthly_data["Date"].dt.to_period("M")
)

monthly_average = (
    monthly_data
    .groupby("Month")[["PM2.5", "PM10"]]
    .mean()
    .reset_index()
)

monthly_average["Month"] = (
    monthly_average["Month"].astype(str)
)

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=monthly_average["Month"],
        y=monthly_average["PM2.5"],
        name="PM2.5",
        marker_color="#00ffcc"
    )
)

fig.add_trace(
    go.Bar(
        x=monthly_average["Month"],
        y=monthly_average["PM10"],
        name="PM10",
        marker_color="#ff0055"
    )
)

fig.update_layout(
    title="MONTHLY AVERAGE POLLUTANT LEVELS",
    xaxis_title="MONTH",
    yaxis_title="AVERAGE CONCENTRATION (µg/m³)",
    barmode="group"
)

st.plotly_chart(
    style_chart(fig),
    use_container_width=True
)


# -----------------------------------------------------
# D. SEASONAL POLLUTION ANALYSIS
# -----------------------------------------------------

st.markdown("---")

st.subheader("> SEASONAL POLLUTION ANALYSIS")

seasonal_data = district_data.copy()


def get_season(month):

    if month in [12, 1, 2]:
        return "Winter"

    elif month in [3, 4, 5]:
        return "Summer"

    elif month in [6, 7, 8, 9]:
        return "Monsoon"

    return "Post-Monsoon"


seasonal_data["Season"] = (
    seasonal_data["Date"]
    .dt.month
    .apply(get_season)
)

season_order = [
    "Winter",
    "Summer",
    "Monsoon",
    "Post-Monsoon"
]

seasonal_average = (
    seasonal_data
    .groupby("Season")[["PM2.5", "PM10"]]
    .mean()
    .reindex(season_order)
    .dropna()
    .reset_index()
)

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=seasonal_average["Season"],
        y=seasonal_average["PM2.5"],
        name="PM2.5",
        marker_color="#00ffcc"
    )
)

fig.add_trace(
    go.Bar(
        x=seasonal_average["Season"],
        y=seasonal_average["PM10"],
        name="PM10",
        marker_color="#ff0055"
    )
)

fig.update_layout(
    title="SEASONAL POLLUTION DISTRIBUTION",
    xaxis_title="SEASON",
    yaxis_title="AVERAGE CONCENTRATION (µg/m³)",
    barmode="group"
)

st.plotly_chart(
    style_chart(fig),
    use_container_width=True
)

st.caption(
    "Seasonal averages use all available observations "
    "for the selected district."
)
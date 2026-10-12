import os
from datetime import date

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg
import streamlit as st


# ---------------------------------------------------------------------
# Page setup and visual theme
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="Weather | Morocco",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
)

SKY = "#2389F2"
NAVY = "#16324F"
MUTED = "#64748B"
RISK_COLORS = {
    "Faible": "#16A34A",
    "Modéré": "#D99A00",
    "Élevé": "#EA580C",
    "Très élevé": "#DC2626",
}

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --sky: #2389F2;
        --sky-light: #EAF5FF;
        --ink: #16324F;
        --muted: #64748B;
        --line: #E5EDF5;
        --surface: #FFFFFF;
    }
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    .stApp {
        background: linear-gradient(180deg, #F4F9FF 0%, #F8FAFC 340px, #F8FAFC 100%);
        color: var(--ink);
    }
    [data-testid="stHeader"] {
        background: rgba(244, 249, 255, 0.85);
    }
    [data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--ink);
        font-family: 'Manrope', sans-serif;
    }
    .block-container {
        max-width: 1440px;
        padding-top: 1.8rem;
        padding-bottom: 3rem;
    }
    h1, h2, h3 {
        color: var(--ink);
        font-family: 'Manrope', sans-serif !important;
        letter-spacing: -0.035em;
    }
    h2 { font-size: 1.35rem !important; }
    h3 { font-size: 1.05rem !important; }
    p, label, .stCaption { color: var(--muted); }
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid var(--line);
        padding: 18px 20px;
        border-radius: 18px;
        box-shadow: 0 5px 18px rgba(22, 50, 79, 0.035);
    }
    div[data-testid="stMetricLabel"] {
        color: #64748B;
        font-size: 0.84rem;
    }
    div[data-testid="stMetricValue"] {
        color: var(--ink);
        font-family: 'Manrope', sans-serif;
        font-weight: 800;
    }
    div[data-testid="stPlotlyChart"] {
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 8px 8px 0 8px;
        box-shadow: 0 5px 18px rgba(22, 50, 79, 0.025);
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        border-radius: 16px;
        overflow: hidden;
    }
    .hero {
        position: relative;
        overflow: hidden;
        border-radius: 26px;
        padding: 28px 32px;
        color: white;
        background: linear-gradient(120deg, #1675D1 0%, #3298F6 56%, #73C7F8 100%);
        box-shadow: 0 14px 36px rgba(35, 137, 242, 0.18);
        margin-bottom: 22px;
    }
    .hero:after {
        content: "";
        position: absolute;
        width: 260px; height: 260px;
        right: -45px; top: -105px;
        border-radius: 50%;
        background: rgba(255,255,255,0.12);
    }
    .hero-kicker {
        color: rgba(255,255,255,0.82);
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: .13em;
        font-weight: 700;
    }
    .hero-title {
        font-family: 'Manrope', sans-serif;
        color: #FFFFFF;
        font-size: clamp(1.7rem, 3vw, 2.55rem);
        line-height: 1.15;
        font-weight: 800;
        letter-spacing: -.045em;
        margin: 7px 0 9px 0;
    }
    .hero-subtitle {
        color: rgba(255,255,255,0.86);
        font-size: .98rem;
        max-width: 660px;
    }
    .hero-date {
        display: inline-block;
        margin-top: 16px;
        padding: 7px 12px;
        border: 1px solid rgba(255,255,255,.3);
        border-radius: 999px;
        background: rgba(255,255,255,.13);
        color: white;
        font-size: .82rem;
    }
    .section-heading {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 28px 0 12px 0;
        color: var(--ink);
        font-family: 'Manrope', sans-serif;
        font-size: 1.24rem;
        font-weight: 800;
        letter-spacing: -.03em;
    }
    .section-dot {
        display: inline-block;
        width: 9px; height: 9px;
        border-radius: 50%;
        background: var(--sky);
        box-shadow: 0 0 0 5px #E2F1FF;
    }
    .forecast-card {
        min-height: 150px;
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 16px 14px;
        text-align: center;
        box-shadow: 0 5px 18px rgba(22,50,79,.03);
    }
    .forecast-day { color: #64748B; font-size: .78rem; font-weight: 600; }
    .forecast-icon { font-size: 1.65rem; margin: 9px 0; }
    .forecast-temp { color: var(--ink); font-size: 1.13rem; font-weight: 800; }
    .forecast-extra { color: #64748B; font-size: .76rem; margin-top: 6px; }
    .risk-pill {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 999px;
        font-size: .76rem;
        font-weight: 700;
    }
    .footer-note {
        color: #8493A5;
        font-size: .78rem;
        text-align: center;
        padding-top: 22px;
    }
    button[kind="primary"] {
        background: var(--sky);
        border: 0;
        border-radius: 12px;
    }
    @media (max-width: 700px) {
        .block-container { padding-top: 1rem; }
        .hero { padding: 22px; border-radius: 20px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------
# Data access: processed Gold records in PostgreSQL
# ---------------------------------------------------------------------
@st.cache_data(ttl=300)
def load_weather_data():
    connection = psycopg.connect(
        host="postgres",
        port="5432",
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        connect_timeout=5,
    )

    query = """
        SELECT DISTINCT
            c.city,
            c.lat,
            c.lng,
            w.date,
            w.temperature_max,
            w.temperature_min,
            w.precipitation_sum,
            w.precipitation_probability_max,
            w.wind_speed_max,
            w.wind_gusts_max,
            w.risk_score,
            w.risk_category,
            w.precipitation_risk,
            w.wind_risk,
            w.temperature_risk
        FROM weather AS w
        JOIN city AS c ON c.id = w.city_id
        ORDER BY w.date, c.city
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [column.name for column in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
    finally:
        connection.close()

    if not df.empty:
        # Defensive safeguard: remove exact duplicate forecast records returned by PostgreSQL.
        # The source table should ideally enforce uniqueness for each city/date forecast.
        df = df.drop_duplicates().reset_index(drop=True)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        numeric_columns = [
            "lat", "lng", "temperature_max", "temperature_min",
            "precipitation_sum", "precipitation_probability_max",
            "wind_speed_max", "wind_gusts_max", "risk_score",
            "precipitation_risk", "wind_risk", "temperature_risk",
        ]
        for column in numeric_columns:
            if column in df.columns:
                df[column] = pd.to_numeric(df[column], errors="coerce")
    return df


def section(title):
    st.markdown(
        f'<div class="section-heading"><span class="section-dot"></span>{title}</div>',
        unsafe_allow_html=True,
    )


def chart_layout(fig, height=330):
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=12, r=12, t=35, b=12),
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(family="DM Sans, sans-serif", color="#64748B", size=12),
        title_font=dict(family="Manrope, sans-serif", size=15, color="#16324F"),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="left", x=0, bgcolor="rgba(255,255,255,0)",
        ),
        hoverlabel=dict(bgcolor="#16324F", font_color="#FFFFFF"),
    )
    fig.update_xaxes(showgrid=False, linecolor="#E5EDF5", zeroline=False)
    fig.update_yaxes(gridcolor="#EDF2F7", linecolor="rgba(0,0,0,0)", zeroline=False)
    return fig


# ---------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------
with st.sidebar:
    st.markdown("## ☀️ Weatherly")
    st.caption("MOROCCO · WEATHER INTELLIGENCE")
    st.divider()

    if st.button("↻  Refresh forecast data", use_container_width=True):
        load_weather_data.clear()
        st.rerun()

    st.markdown("### Explore")
    st.caption("Filter the forecast data shown across the dashboard.")
    st.markdown("---")
    st.caption("Data source")
    st.markdown("**Open-Meteo → PostgreSQL Gold**")
    st.caption("Refreshes automatically every 5 minutes.")


# ---------------------------------------------------------------------
# Load and validate data
# ---------------------------------------------------------------------
try:
    df = load_weather_data()
except Exception as exc:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">Weather intelligence · Morocco</div>
            <div class="hero-title">Your forecast, at a glance.</div>
            <div class="hero-subtitle">Connect to the weather data store to explore forecast conditions and delivery risk.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.error(
        "Unable to load weather data from PostgreSQL. Check the database configuration "
        "and ensure the ETL pipeline has initialized the Gold tables."
    )
    with st.expander("Technical details"):
        st.code(str(exc))
    st.stop()

if df.empty:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">Weather intelligence · Morocco</div>
            <div class="hero-title">Your forecast, at a glance.</div>
            <div class="hero-subtitle">A clear view of upcoming weather and potential delivery disruption.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info("No forecast records are available yet. Run the ETL pipeline, then refresh the dashboard.")
    st.stop()


# ---------------------------------------------------------------------
# Filters
# ---------------------------------------------------------------------
with st.sidebar:
    cities = sorted(df["city"].dropna().unique().tolist())
    selected_cities = st.multiselect("Cities", options=cities, default=cities)

    risk_levels = sorted(df["risk_category"].dropna().unique().tolist())
    risk_default = [risk for risk in ["Faible", "Modéré", "Élevé", "Très élevé"] if risk in risk_levels]
    selected_risks = st.multiselect(
        "Risk levels",
        options=risk_levels,
        default=risk_default or risk_levels,
    )

    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    date_range = st.date_input(
        "Forecast dates",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

if not selected_cities or not selected_risks:
    st.info("Choose at least one city and one risk level in the sidebar.")
    st.stop()

if not isinstance(date_range, (tuple, list)) or len(date_range) != 2:
    st.info("Choose both a start date and an end date in the sidebar.")
    st.stop()

start_date, end_date = date_range
filtered = df[
    df["city"].isin(selected_cities)
    & df["risk_category"].isin(selected_risks)
    & df["date"].dt.date.between(start_date, end_date)
].copy()

if filtered.empty:
    st.warning("No forecast records match these filters. Try selecting more cities, risk levels, or dates.")
    st.stop()

filtered = filtered.sort_values(["date", "city"])
latest_date = filtered["date"].max()
latest = filtered[filtered["date"] == latest_date]
latest_city_count = latest["city"].nunique()
average_risk = filtered["risk_score"].mean()
highest_risk = filtered["risk_score"].max()
high_risk_count = filtered["risk_category"].isin(["Élevé", "Très élevé"]).sum()

# City selection drives the visual forecast summary; no current weather is fabricated.
hero_city = st.selectbox(
    "Featured city",
    options=sorted(filtered["city"].dropna().unique().tolist()),
    index=0,
    help="Choose a city to feature in the weather overview.",
)
city_forecast = filtered[filtered["city"] == hero_city].sort_values("date")
featured = city_forecast.iloc[-1]
featured_date = featured["date"]
risk_label = str(featured["risk_category"])
risk_color = RISK_COLORS.get(risk_label, SKY)
temp_max = featured["temperature_max"]
temp_min = featured["temperature_min"]


# ---------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------
hero_left, hero_right = st.columns([1.7, 1], vertical_alignment="center")
with hero_left:
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-kicker">☀ &nbsp; WEATHER INTELLIGENCE · MOROCCO</div>
            <div class="hero-title">A clearer view of the days ahead.</div>
            <div class="hero-subtitle">
                Explore the forecast, compare cities, and spot weather conditions
                that could affect deliveries.
            </div>
            <div class="hero-date">📍 {hero_city} &nbsp; · &nbsp; Forecast for {featured_date:%A, %d %B %Y}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with hero_right:
    risk_pill = (
        f'<span class="risk-pill" style="color:{risk_color};background:{risk_color}18;">'
        f'{risk_label} weather risk</span>'
    )
    st.markdown(
        f"""
        <div style="background:#FFFFFF;border:1px solid #E5EDF5;border-radius:24px;
                    padding:24px 25px;min-height:190px;box-shadow:0 8px 24px rgba(22,50,79,.045);">
            <div style="color:#64748B;font-size:.82rem;font-weight:600;">LATEST FORECAST · {hero_city}</div>
            <div style="display:flex;align-items:center;gap:13px;margin:15px 0 8px;">
                <div style="font-size:2.5rem;">🌤️</div>
                <div>
                    <div style="font-family:Manrope,sans-serif;font-size:2.35rem;line-height:1;
                                color:#16324F;font-weight:800;">
                        {f"{temp_max:.0f}°" if pd.notna(temp_max) else "—"}
                    </div>
                    <div style="color:#64748B;font-size:.88rem;">
                        High &nbsp;·&nbsp; Low {f"{temp_min:.0f}°" if pd.notna(temp_min) else "—"}
                    </div>
                </div>
            </div>
            {risk_pill}
            <div style="color:#64748B;font-size:.8rem;margin-top:12px;">
                Forecast data, not live observations
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# KPI cards
section("Forecast overview")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Cities in view", f"{filtered['city'].nunique()}", help="Unique cities in the selected forecast.")
k2.metric("Forecast records", f"{len(filtered):,}", help="City-day records after applying your filters.")
k3.metric("High-risk records", f"{int(high_risk_count):,}", help="Records classified as Élevé or Très élevé.")
k4.metric("Average risk score", f"{average_risk:.1f}/100" if pd.notna(average_risk) else "—")

# Seven-day style forecast cards (one card per date for the selected featured city)
section(f"{hero_city} · Daily forecast")
featured_days = city_forecast.sort_values("date").head(7)
cols = st.columns(max(1, len(featured_days)))
for col, (_, row) in zip(cols, featured_days.iterrows()):
    row_risk = str(row["risk_category"])
    row_color = RISK_COLORS.get(row_risk, SKY)
    hi = f"{row['temperature_max']:.0f}°" if pd.notna(row["temperature_max"]) else "—"
    lo = f"{row['temperature_min']:.0f}°" if pd.notna(row["temperature_min"]) else "—"
    rain = f"{row['precipitation_probability_max']:.0f}%" if pd.notna(row["precipitation_probability_max"]) else "—"
    wind = f"{row['wind_speed_max']:.0f}" if pd.notna(row["wind_speed_max"]) else "—"
    with col:
        st.markdown(
            f"""
            <div class="forecast-card">
                <div class="forecast-day">{row['date']:%a · %d %b}</div>
                <div class="forecast-icon">{"🌧️" if (pd.notna(row["precipitation_sum"]) and row["precipitation_sum"] >= 2) else "☀️"}</div>
                <div class="forecast-temp">{hi} <span style="color:#94A3B8;font-weight:500;">/ {lo}</span></div>
                <div class="forecast-extra">💧 {rain} &nbsp; · &nbsp; 💨 {wind} km/h</div>
                <div style="margin-top:10px;color:{row_color};font-size:.74rem;font-weight:700;">{row_risk} risk</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------------------
# Risk analytics
# ---------------------------------------------------------------------
section("Weather risk trends")
daily_risk = (
    filtered.groupby(["date", "city"], as_index=False)["risk_score"]
    .mean()
)
fig_risk = px.line(
    daily_risk,
    x="date",
    y="risk_score",
    color="city",
    markers=True,
    labels={"date": "Forecast date", "risk_score": "Risk score (0–100)", "city": "City"},
)
fig_risk.update_yaxes(range=[0, 100])
fig_risk.update_traces(line=dict(width=2.5), marker=dict(size=6))
st.plotly_chart(chart_layout(fig_risk, 350), use_container_width=True)

section("Weather conditions")
temperature_tab, precipitation_tab, wind_tab = st.tabs(
    ["🌡️  Temperature", "💧  Precipitation", "💨  Wind"]
)

with temperature_tab:
    temperature = filtered.groupby("date", as_index=False).agg(
        temperature_max=("temperature_max", "mean"),
        temperature_min=("temperature_min", "mean"),
    )
    fig_temperature = go.Figure()
    fig_temperature.add_trace(
        go.Scatter(
            x=temperature["date"], y=temperature["temperature_max"],
            mode="lines+markers", name="Average high",
            line=dict(color="#F59E0B", width=3),
            marker=dict(size=7), fill=None,
        )
    )
    fig_temperature.add_trace(
        go.Scatter(
            x=temperature["date"], y=temperature["temperature_min"],
            mode="lines+markers", name="Average low",
            line=dict(color="#2389F2", width=3),
            marker=dict(size=7),
        )
    )
    fig_temperature.update_layout(
        title="Average daily high and low",
        xaxis_title=None,
        yaxis_title="Temperature (°C)",
    )
    st.plotly_chart(chart_layout(fig_temperature), use_container_width=True)

with precipitation_tab:
    precipitation = filtered.groupby("date", as_index=False).agg(
        precipitation_sum=("precipitation_sum", "mean"),
        precipitation_probability_max=("precipitation_probability_max", "mean"),
    )
    fig_precipitation = px.bar(
        precipitation, x="date", y="precipitation_sum",
        labels={"date": "Forecast date", "precipitation_sum": "Precipitation (mm)"},
        title="Average daily precipitation",
        color_discrete_sequence=[SKY],
    )
    fig_precipitation.update_traces(marker_line_width=0, opacity=.88)
    st.plotly_chart(chart_layout(fig_precipitation), use_container_width=True)
    st.caption("Precipitation is averaged across the selected cities. The table below contains city-level values.")

with wind_tab:
    wind = filtered.groupby("date", as_index=False).agg(
        wind_speed_max=("wind_speed_max", "mean"),
        wind_gusts_max=("wind_gusts_max", "mean"),
    )
    fig_wind = px.line(
        wind, x="date", y=["wind_speed_max", "wind_gusts_max"],
        markers=True,
        labels={"date": "Forecast date", "value": "Wind speed (km/h)", "variable": "Measure"},
        title="Average wind and gust conditions",
        color_discrete_sequence=["#2389F2", "#8B5CF6"],
    )
    fig_wind.update_traces(line=dict(width=3), marker=dict(size=6))
    st.plotly_chart(chart_layout(fig_wind), use_container_width=True)

# ---------------------------------------------------------------------
# City comparison and detail table
# ---------------------------------------------------------------------
section("City risk comparison")
ranking = (
    filtered.groupby("city", as_index=False)
    .agg(
        average_risk=("risk_score", "mean"),
        maximum_risk=("risk_score", "max"),
        precipitation_mm=("precipitation_sum", "max"),
        maximum_wind_kmh=("wind_speed_max", "max"),
        maximum_temperature_c=("temperature_max", "max"),
    )
    .sort_values("average_risk", ascending=True)
)
fig_ranking = px.bar(
    ranking, x="average_risk", y="city", orientation="h",
    color="average_risk", color_continuous_scale=["#86EFAC", "#FDE68A", "#FB923C", "#DC2626"],
    range_color=(0, 100),
    labels={"average_risk": "Average risk score", "city": "City"},
)
fig_ranking.update_layout(coloraxis_colorbar_title="Risk", yaxis_title=None, xaxis_title="Average risk score")
fig_ranking.update_traces(marker_line_width=0, opacity=.92)
st.plotly_chart(chart_layout(fig_ranking, max(300, 36 * len(ranking) + 80)), use_container_width=True)

section("Detailed forecast")
display_columns = [
    "city", "date", "temperature_min", "temperature_max",
    "precipitation_sum", "precipitation_probability_max",
    "wind_speed_max", "risk_score", "risk_category",
]
table = filtered[display_columns].sort_values(["date", "risk_score"], ascending=[True, False]).copy()
st.dataframe(
    table,
    use_container_width=True,
    hide_index=True,
    column_config={
        "city": st.column_config.TextColumn("City"),
        "date": st.column_config.DateColumn("Forecast date", format="ddd, DD MMM"),
        "temperature_min": st.column_config.NumberColumn("Low (°C)", format="%.1f"),
        "temperature_max": st.column_config.NumberColumn("High (°C)", format="%.1f"),
        "precipitation_sum": st.column_config.NumberColumn("Rain (mm)", format="%.1f"),
        "precipitation_probability_max": st.column_config.NumberColumn("Rain chance", format="%.0f%%"),
        "wind_speed_max": st.column_config.NumberColumn("Wind (km/h)", format="%.1f"),
        "risk_score": st.column_config.ProgressColumn("Risk score", min_value=0, max_value=100, format="%.0f"),
        "risk_category": st.column_config.TextColumn("Risk level"),
    },
)
csv_data = table.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️  Download filtered forecast (CSV)",
    data=csv_data,
    file_name="morocco_weather_forecast.csv",
    mime="text/csv",
    use_container_width=False,
)

st.markdown(
    """
    <div class="footer-note">
        Weatherly · Morocco Weather Intelligence<br>
        Delivery-risk indicators are decision-support estimates based on forecast variables,
        not official meteorological warnings.
    </div>
    """,
    unsafe_allow_html=True,
)

import pandas as pd

# =================================
# Temperature Category
# =================================


def temperature_category(temp):
    if temp < 5:
        return "Très froid"
    elif temp < 15:
        return "Froid"
    elif temp < 25:
        return "Modérée"
    elif temp < 35:
        return "Chaud"
    else:
        return "Très chaud"


# =================================
# Precipitation Category
# =================================


def precipitation_category(rain):
    if rain == 0:
        return "Aucune"
    elif rain < 5:
        return "Faible"
    elif rain < 20:
        return "Modérée"
    else:
        return "Forte"


# =================================
# Wind Category
# =================================


def wind_category(wind):
    if wind < 20:
        return "Faible"
    elif wind < 40:
        return "Modéré"
    elif wind < 60:
        return "Fort"
    else:
        return "Très fort"


# =================================
# Risk Score
# =================================


def precipitation_risk(rain):
    if rain == 0:
        return 0
    elif rain < 5:
        return 25
    elif rain < 20:
        return 60
    else:
        return 100


def wind_risk(wind):
    if wind < 20:
        return 0
    elif wind < 40:
        return 30
    elif wind < 60:
        return 70
    else:
        return 100


def temperature_risk(temp):
    if 15 <= temp <= 25:
        return 0
    elif 10 <= temp < 15 or 25 < temp <= 30:
        return 30
    elif 5 <= temp < 10 or 30 < temp <= 35:
        return 60
    else:
        return 100


def calculate_risk_score(df):

    df["precipitation_risk"] = df["precipitation_sum"].apply(precipitation_risk)

    df["wind_risk"] = df["wind_speed_max"].apply(wind_risk)

    df["temperature_risk"] = df["temperature_max"].apply(temperature_risk)

    df["risk_score"] = (
        df["precipitation_risk"] * 0.40
        + df["wind_risk"] * 0.35
        + df["temperature_risk"] * 0.25
    ).round()

    return df


# =================================
# Risk Category
# =================================


def risk_category(score):

    if score < 25:
        return "Faible"
    elif score < 50:
        return "Modéré"
    elif score < 75:
        return "Élevé"
    else:
        return "Très élevé"


# =================================
# Feature Engineering
# =================================


def create_features(df):

    df["temperature_category"] = df["temperature_max"].apply(temperature_category)

    df["precipitation_category"] = df["precipitation_sum"].apply(precipitation_category)

    df["wind_category"] = df["wind_speed_max"].apply(wind_category)

    df = calculate_risk_score(df)

    df["risk_category"] = df["risk_score"].apply(risk_category)

    return df


# =================================
# Save Gold
# =================================


def save_gold(df, path):

    df.to_csv(path, index=False)


# =================================
# Run Gold
# =================================


def run_gold(silver_path, gold_path):

    df = load_silver(silver_path)

    df = create_features(df)

    save_gold(df, gold_path)

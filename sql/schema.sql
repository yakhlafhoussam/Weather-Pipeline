CREATE TABLE IF NOT EXISTS city (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    city_ascii VARCHAR(100),
    lat NUMERIC(9,6),
    lng NUMERIC(9,6),
    country VARCHAR(100),
    iso2 VARCHAR(2),
    admin_name VARCHAR(100),
    capital VARCHAR(50),
    population BIGINT
);

CREATE TABLE IF NOT EXISTS weather (
    id SERIAL PRIMARY KEY,
    city_id BIGINT NOT NULL,
    date DATE NOT NULL,

    temperature_max NUMERIC(5,2),
    temperature_min NUMERIC(5,2),
    precipitation_sum NUMERIC(6,2),
    precipitation_probability_max INTEGER,
    wind_speed_max NUMERIC(6,2),
    wind_gusts_max NUMERIC(6,2),
    weather_code INTEGER,

    temperature_category VARCHAR(30),
    precipitation_category VARCHAR(30),
    wind_category VARCHAR(30),

    precipitation_risk INTEGER,
    wind_risk INTEGER,
    temperature_risk INTEGER,
    risk_score NUMERIC(5,2),
    risk_category VARCHAR(30),

    CONSTRAINT fk_weather_city
        FOREIGN KEY (city_id)
        REFERENCES city(id),

    CONSTRAINT unique_city_date
        UNIQUE (city_id, date)
);
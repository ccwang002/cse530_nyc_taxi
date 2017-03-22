CREATE TABLE weather (
    id                  SERIAL PRIMARY KEY,
    station             VARCHAR(3),
    record_datetime     TIMESTAMP WITH TIME ZONE,
    temperature         NUMERIC,    -- °C
    dew_temperature     NUMERIC,    -- °C
    relative_humidity   NUMERIC,    -- %
    wind_direction      NUMERIC,    -- degree from north
    wind_speed          NUMERIC,    -- miles per hour
    one_hour_acc_precipitation  NUMERIC,    -- mm
    visibility          NUMERIC,    -- miles
    wind_gust_speed     NUMERIC     -- miles per hour
);

CREATE INDEX weather_station_record_datetime_btree
    ON weather (station, record_datetime);

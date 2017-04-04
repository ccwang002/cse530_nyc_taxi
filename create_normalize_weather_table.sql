CREATE TABLE weather_normalize (
    id                  SERIAL PRIMARY KEY,
    station             VARCHAR(3),
    record_datetime     TIMESTAMP WITH TIME ZONE,
    temperature         NUMERIC,    -- °C
    one_hour_acc_precipitation  NUMERIC    -- mm
);

CREATE INDEX weather_normalize_station_record_datetime_btree
    ON weather_normalize (station, record_datetime);

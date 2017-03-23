CREATE TABLE taxi_trips (
    id                  SERIAL PRIMARY KEY,
    taxi_type           VARCHAR(16),
    vendor_id           INTEGER,
    pickup_datetime     TIMESTAMP WITH TIME ZONE,
    dropoff_datetime    TIMESTAMP WITH TIME ZONE,
    passenger_count     INTEGER,
    trip_distance       NUMERIC,
    pickup_lon          NUMERIC,
    pickup_lat          NUMERIC,
    rate_code_id        INTEGER,
    store_and_fwd_flag  VARCHAR(1),
    dropoff_lon         NUMERIC,
    dropoff_lat         NUMERIC,
    payment_type        INTEGER,
    fare_amount         NUMERIC,
    extra               NUMERIC,
    mta_tax             NUMERIC,
    tip_amount          NUMERIC,
    tolls_amount        NUMERIC,
    improvement_surcharge   NUMERIC,
    total_amount        NUMERIC
);

CREATE INDEX taxi_trips_pickup_datetime_ix
    ON  taxi_trips (pickup_datetime);

CREATE INDEX taxi_trips_dropoff_datetime_ix
    ON  taxi_trips (dropoff_datetime);

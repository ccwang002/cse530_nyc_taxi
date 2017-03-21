SELECT AddGeometryColumn('taxi_trips', 'pickup_loc', 4326, 'POINT', 2);
SELECT AddGeometryColumn('taxi_trips', 'dropoff_loc', 4326, 'POINT', 2);

UPDATE taxi_trips
SET pickup_loc = ST_SetSRID(ST_MakePoint(pickup_lon, pickup_lat), 4326),
    dropoff_loc = ST_SetSRID(ST_MakePoint(dropoff_lon, dropoff_lat), 4326);

CREATE INDEX taxi_trips_pickup_gist
  ON taxi_trips
  USING gist (pickup_loc);

CREATE INDEX taxi_trips_dropoff_gist
  ON taxi_trips
  USING gist (dropoff_loc);

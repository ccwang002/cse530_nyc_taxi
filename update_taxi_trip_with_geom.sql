SELECT AddGeometryColumn('taxi_trips', 'pickup_loc', 3627, 'POINT', 2);
SELECT AddGeometryColumn('taxi_trips', 'dropoff_loc', 3627, 'POINT', 2);

UPDATE taxi_trips
SET pickup_loc = ST_Transform(ST_SetSRID(ST_MakePoint(pickup_lon, pickup_lat), 4326), 3627),
    dropoff_loc = ST_Transform(ST_SetSRID(ST_MakePoint(dropoff_lon, dropoff_lat), 4326), 3627);

CREATE INDEX taxi_trips_pickup_gist
  ON taxi_trips
  USING gist (pickup_loc);

CREATE INDEX taxi_trips_dropoff_gist
  ON taxi_trips
  USING gist (dropoff_loc);

#!/usr/bin/env bash

readonly DB_NAME="liang-bo.wang_project1"

call_psql () {
    psql -d "$DB_NAME" "$@"
}

shp2pgsql -s 2263:3627 taxi_zones/taxi_zones.shp | call_psql
call_psql -c "CREATE INDEX index_taxi_zones_on_geom ON taxi_zones USING gist (geom);"
call_psql -c "CREATE INDEX index_taxi_zones_on_locationid ON taxi_zones (locationid);"
call_psql -c "VACUUM ANALYZE taxi_zones;"

shp2pgsql -s 2263:3627 nyct2010_17a/nyct2010.shp | call_psql
# call_psql -f add_newark_airport.sql
call_psql -c "CREATE INDEX index_nyct_on_geom ON nyct2010 USING gist (geom);"
call_psql -c "CREATE INDEX index_nyct_on_ntacode ON nyct2010 (ntacode);"
call_psql -c "VACUUM ANALYZE nyct2010;"

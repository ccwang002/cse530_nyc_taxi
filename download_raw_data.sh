cat raw_taxi_trip_data_urls.txt | xargs -n 1 -P 3 wget -c -P raw_trip_data/

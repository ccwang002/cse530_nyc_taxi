library(stringr)
library(dplyr)
library(readr)
library(ggplot2)
library(ggmap)
library(viridis)

trips_to_jfk <- readr::read_csv('trips_to_jfk_201606.csv')

manhattan <- c(
    left = -74.015, right = -73.965,
    bottom = 40.73, top = 40.775
)
map <- get_stamenmap(manhattan, zoom = 13, maptype = "toner-hybrid")
ggmap(map)

# Pick up location 
g_to_jfk <- qmplot(
  pickup_lon, pickup_lat, 
  data = trips_to_jfk, 
  geom = "blank", 
  zoom = 11, 
  maptype = "toner", 
  darken = .7, 
  legend = "bottomleft"
)
f <- g_to_jfk +
  geom_point(color = "red", alpha = 0.1, size = 0.05)
f
ggsave("jfk_pickup_full_dots.png", width = 9, height = 9)

f <- g_to_jfk + 
  stat_density_2d(aes(fill = ..level..), geom = "polygon", alpha = .3, color = NA, n = 400) +
  scale_fill_viridis("Pickup\nLocation")
f
ggsave("jfk_pickup_full.png", width = 9, height = 9)

manhattan_pickup_only <- trips_to_jfk %>% 
  filter(
    pickup_lon >= -74.015 & pickup_lon <= -73.965 &
      pickup_lat >= 40.73 & pickup_lat <= 40.775
  )
g_to_manhattan <- qmplot(
  pickup_lon, pickup_lat, 
  data = manhattan_pickup_only, 
  geom = "blank", 
  zoom = 14, 
  maptype = "toner", 
  darken = .7, 
  legend = "topleft"
)

f <- g_to_manhattan +
  geom_point(color = "red", alpha = 0.3, size = 0.1)
f
ggsave("manhattan_to_jfk_dots.png", width = 6, height = 8)

f <- g_to_manhattan +
  stat_density_2d(aes(fill = ..level..), geom = "polygon", alpha = .3, color = NA, n = 200) +
  scale_fill_viridis("Pickup\nLocation")
f
ggsave("manhattan_to_jfk.png", width = 6, height = 8)


manhattan_core <- c(
  left = -73.974, right = -73.970,
  bottom = 40.755, top = 40.76
)
map <- get_stamenmap(manhattan_core, zoom = 17, maptype = "toner-hybrid")
ggmap(map)

manhattan_core_pickup_only <- trips_to_jfk %>% 
  filter(
    pickup_lon >= -73.976 & pickup_lon <= -73.968 &
      pickup_lat >= 40.751 & pickup_lat <= 40.759
  )
g_to_manhattan_core <- qmplot(
  pickup_lon, pickup_lat, 
  data = manhattan_core_pickup_only, 
  geom = "blank", 
  zoom = 17, 
  maptype = "roadmap",
  mapcolor = "bw",
  source = "google",
  darken = .2, 
  legend = "bottomleft"
)
f <- g_to_manhattan_core + geom_point(color="red", alpha = 0.5, size = 1.2)
f
ggsave("manhattan_E48st_lexington_pickup_dots.png", width = 7, height = 7)

f <- g_to_manhattan_core + 
  coord_cartesian() + 
  geom_hex(alpha = 0.7) +
  scale_fill_viridis("Pickup\nLocation")
f
ggsave("manhattan_E48st_lexington_pickup.png", width = 7, height = 7)


# Times square 40.758927, -73.985123
manhattan_times_square <- c(
  left = -73.989, right = -73.981,
  bottom = 40.757, top = 40.761
)
map <- get_stamenmap(manhattan_times_square, zoom = 17, maptype = "toner-hybrid")
ggmap(map)

manhattan_times_square_pickup_only <- trips_to_jfk %>% 
  filter(
    pickup_lon >= -73.989 & pickup_lon <= -73.981 &
      pickup_lat >= 40.754 & pickup_lat <= 40.764
  )
g_from_timessq <- qmplot(
  pickup_lon, pickup_lat, 
  data = manhattan_times_square_pickup_only, 
  geom = "blank", 
  zoom = 17, 
  maptype = "roadmap",
  mapcolor = "bw",
  source = "google",
  darken = .2, 
  legend = "bottomleft"
)
f <- g_from_timessq + geom_point(color="red", alpha = 0.5, size = 1.2)
f
ggsave("manhattan_times_square_pickup_dots.png", width = 7, height = 7)

f <- g_from_timessq + 
  coord_cartesian() + 
  geom_hex(alpha = 0.7, bins = 40) +
  scale_fill_viridis("Pickup\nLocation")
f 
ggsave("manhattan_times_square_pickup.png", width = 7, height = 7)

# Find where airport is
jfk_airport <- c(
  left = -73.793, right = -73.776,
  bottom = 40.640, top = 40.651
)
map <- get_stamenmap(jfk_airport, zoom = 16, maptype = "toner-hybrid")
ggmap(map)

# Drop off location 
jfk_dropoff_only <- trips_to_jfk %>% 
  filter(
    dropoff_lon >= -73.793 & dropoff_lon <= -73.776 &
    dropoff_lat >= 40.640 & dropoff_lat <= 40.651
  )
  
f <- qmplot(
  dropoff_lon, dropoff_lat, 
  data = jfk_dropoff_only, 
  geom = "blank", 
  zoom = 16, 
  maptype = "toner-hybrid", 
  legend = "topleft"
) +
  stat_density_2d(aes(fill = ..level..), geom = "polygon", alpha = .3, color = NA, n = 200) +
  scale_fill_gradient2("Dropoff\nLocation", low = "white", mid = "yellow", high = "red", midpoint = 600)
f
ggsave("jfk_dropoff.png", width = 9, height = 7.5)

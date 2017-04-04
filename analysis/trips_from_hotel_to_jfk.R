library(stringr)
library(dplyr)
library(readr)
library(ggplot2)

trips_to_jfk <- readr::read_csv('trips_New_York_Marriott_Marquis_to_jfk.csv')
trips_to_jfk <- trips_to_jfk %>%
  mutate(
    pickup_hour = as.integer(str_match(trips_to_jfk$pickup_datetime, '\\d{4}-\\d{2}-\\d{2} (\\d{2}):')[, 2])
  ) %>%
  mutate(
    is_rush_hour = (pickup_hour >= 17) & (pickup_hour <= 20)
  )

model <- lm(
  trip_duration ~ pickup_hour + is_rush_hour + max_precipitation + pickup_hour:max_precipitation +  avg_temperature,
  data = trips_to_jfk
)
summary(model)



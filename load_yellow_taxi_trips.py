import argparse
from collections import namedtuple
from datetime import datetime
from io import BytesIO, StringIO
import logging
from pathlib import Path

import pandas as pd
import pytz
import psycopg2
from pgcopy import CopyManager, Replace

logger = logging.getLogger(__name__)
UTC = pytz.UTC
EST = pytz.timezone('US/Eastern')


def make_nyc_dt(dt_str):
    dt = UTC.normalize(
        EST.localize(datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S'))
    )
    return dt


YELLOW_COLS = [
    'vendor_id', 'pickup_datetime', 'dropoff_datetime',
    'passenger_count', 'trip_distance',
    'pickup_lon', 'pickup_lat',
    'rate_code_id', 'store_and_fwd_flag',
    'dropoff_lon', 'dropoff_lat',
    'payment_type', 'fare_amount',
    'extra', 'mta_tax', 'tip_amount', 'tolls_amount',
    'improvement_surcharge', 'total_amount'
]


def read_yellow_trip(csv_pth, chunksize=100000):
    df_reader = pd.read_csv(
        csv_pth,
        header=0, index_col=False, usecols=range(19),
        chunksize=chunksize, parse_dates=False,
        names=YELLOW_COLS
    )
    for i, df in enumerate(df_reader):
        logger.info(f'Reading chunck {i * chunksize} - {(i + 1) * chunksize}')
        yield df


def load_yellow_trip_to_db(csv_pth, conn, mgr):
    for df in read_yellow_trip(csv_pth):
        # Create DB records
        records = []
        for trip in df.itertuples(index=False, name='YellowTrip'):
            tup = trip._replace(
                pickup_datetime=make_nyc_dt(trip.pickup_datetime),
                dropoff_datetime=make_nyc_dt(trip.dropoff_datetime),
                store_and_fwd_flag=trip.store_and_fwd_flag.encode(),
            )
            records.append((b'YELLOW', *tup))
        # Copy records into DB
        with conn:
            mgr.copy(records, BytesIO)


if __name__ == '__main__':
    # setup console logging
    console = logging.StreamHandler()
    all_loggers = logging.getLogger()
    all_loggers.setLevel(logging.INFO)
    all_loggers.addHandler(console)
    log_fmt = '[%(asctime)s][%(levelname)-7s] %(message)s'
    log_formatter = logging.Formatter(log_fmt, '%Y-%m-%d %H:%M:%S')
    console.setFormatter(log_formatter)

    # setup CLI
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'csv_pth',
        nargs='+',
        help="Path to the trip csv files"
    )
    parser.add_argument(
        "--db-name",
        default='liang-bo.wang_project1',
        help="Path to the trip csv files"
    )
    args = parser.parse_args()

    # Make sure all the CSV files existed
    for pth in args.csv_pth:
        if not Path(pth).exists():
            parser.error(f'CSV file {pth} does not exist!')

    # Connect to the DB
    conn = psycopg2.connect(database=args.db_name)
    mgr = CopyManager(conn, 'taxi_trips', ['taxi_type', *YELLOW_COLS])
    for csv_pth in args.csv_pth:
        logger.info(f'Loading CSV {csv_pth}')
        load_yellow_trip_to_db(csv_pth, conn, mgr)
        print(csv_pth)
    conn.close()

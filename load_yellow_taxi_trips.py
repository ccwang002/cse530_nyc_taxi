import argparse
from collections import namedtuple
from datetime import datetime
from decimal import Decimal
from io import BytesIO
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
    return EST.localize(
        datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    )


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

INTEGER_FIELDS = [
    'vendor_id',
    'passenger_count',
    'rate_code_id',
    'payment_type'
]

DATETIME_FIELDS = [
    'pickup_datetime', 'dropoff_datetime',
]

DECIMAL_FIELDS = [
    'trip_distance',
    'pickup_lon', 'pickup_lat',
    'dropoff_lon', 'dropoff_lat',
    'fare_amount', 'extra', 'mta_tax',
    'tip_amount', 'tolls_amount',
    'improvement_surcharge', 'total_amount'
]


def read_yellow_trip(csv_pth, chunksize=100000):
    logger.info(f'Split CSV by chunk size: {chunksize}')
    return pd.read_csv(
        csv_pth,
        header=0,
        names=YELLOW_COLS,
        usecols=range(19),
        index_col=False, parse_dates=False, na_filter=False,
        dtype={
            col: int for col in INTEGER_FIELDS
        },
        converters={
            'store_and_fwd_flag': str.encode,
            **{col: Decimal for col in DECIMAL_FIELDS},
            **{col: make_nyc_dt for col in DATETIME_FIELDS},
            **{col: int for col in INTEGER_FIELDS},
        },
        chunksize=chunksize,
        memory_map=True
    )


def load_yellow_trip_to_db(csv_pth, conn, mgr):
    for i, df in enumerate(read_yellow_trip(csv_pth)):
        logger.info(f'Reading chunk {i}')
        records = [
            (b'YELLOW', *tup)
            for tup in df.itertuples(index=False, name='YellowTrip')
        ]
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

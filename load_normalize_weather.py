import argparse
from datetime import datetime
from decimal import Decimal
from io import BytesIO, StringIO
import logging
from pathlib import Path

import pandas as pd
import pytz
import psycopg2
from pgcopy import CopyManager, Replace

logger = logging.getLogger(__name__)
UTC = pytz.UTC

#changed by sithu
WEATHER_COLS = [
    'station', 'record_datetime',
    'temperature',
    'one_hour_acc_precipitation'
]

#changed by sithu
DECIMAL_FIELDS = [
    'temperature',
    'one_hour_acc_precipitation',
]

to_na_decimal = lambda text: Decimal('NaN') if text == 'M' else Decimal(text)
to_utc_date = lambda text: UTC.localize(datetime.strptime(text, '%Y-%m-%d %H:%M'))


def read_weather(csv_pth, chunksize=20000):
    logger.info(f'Split CSV by chunk size: {chunksize}')
    return pd.read_table(
        csv_pth,
        skiprows=5,
        header=0,
        names=WEATHER_COLS,
        parse_dates=False, index_col=False,
        converters={
            'station': str.encode,
            'record_datetime': to_utc_date,
            **{col: to_na_decimal for col in DECIMAL_FIELDS},
        },
        chunksize=chunksize,
        memory_map=True
    )


def load_weather_to_db(csv_pth, conn, mgr):
    for i, df in enumerate(read_weather(csv_pth)):
        logger.info(f'Reading chuck {i}')
        records = list(df.itertuples(index=True, name='Weather'))
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
        help="Path to the weather csv file"
    )
    parser.add_argument(
        "--db-name",
        default='liang-bo.wang_project1',
        help="Database name"
    )
    args = parser.parse_args()

    # Make sure all the CSV files existed
    if not Path(args.csv_pth).exists():
        parser.error(f'CSV file {pth} does not exist!')
    csv_pth = args.csv_pth

    # Connect to the DB
    conn = psycopg2.connect(database=args.db_name)
    mgr = CopyManager(conn, 'weather_normalize', ['id', *WEATHER_COLS]) #changed by sithu
    logger.info(f'Loading CSV {csv_pth}')
    load_weather_to_db(csv_pth, conn, mgr)
    conn.close()

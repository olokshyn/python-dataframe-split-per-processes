from typing import List
from argparse import ArgumentParser

import numpy as np
import pandas as pd


def read_dataset(no_limits: bool = False) -> pd.DataFrame:
    return pd.read_csv(
        'pubg_events_logplayerattack.csv',
        nrows=None if no_limits else 100000
    )


def split_dataset_into_chunks(
        dataset: pd.DataFrame,
        chunks_num: int
) -> List[pd.DataFrame]:
    chunk_size = len(dataset) // chunks_num
    return [df for _, df in dataset.groupby(np.arange(len(dataset)) // chunk_size)]


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '--proc-num',
        type=int,
        required=True,
        help='Number of processes'
    )
    parser.add_argument(
        '--no-limits',
        default=False,
        action='store_true'
    )
    return parser.parse_args()

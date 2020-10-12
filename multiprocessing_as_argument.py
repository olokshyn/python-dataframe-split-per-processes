from time import sleep
from multiprocessing import Pool

import pandas as pd

from utils import read_dataset, split_dataset_into_chunks, parse_args


def main(proc_num: int, no_limits: bool) -> None:
    df = read_dataset(no_limits)
    chunks = split_dataset_into_chunks(df, proc_num)
    with Pool(proc_num) as pool:
        pool.map(worker, chunks)
    for chunk in chunks:
        print(len(chunk.head()))


def worker(df: pd.DataFrame) -> None:
    print(f'Got chunk with start index {df.index[0]}')
    sleep(10)
    print('Changed data from worker!')
    # Changing df doesn't affect the parent thread
    df[:] = 0
    sleep(10)


if __name__ == '__main__':
    args = parse_args()
    main(args.proc_num, args.no_limits)

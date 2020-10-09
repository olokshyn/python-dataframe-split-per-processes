from time import sleep
from multiprocessing import Pool

from utils import read_dataset, split_dataset_into_chunks, parse_args


_g_chunks = None


def main(proc_num: int, no_limits: bool) -> None:
    df = read_dataset(no_limits)
    chunks = split_dataset_into_chunks(df, proc_num)
    global _g_chunks
    _g_chunks = chunks
    with Pool(proc_num) as pool:
        pool.map(worker, range(len(chunks)))
    for chunk in _g_chunks:
        print(chunk.head())


def worker(chunk_id: int) -> None:
    df = _g_chunks[chunk_id]
    print(f'Read global chunk with start index {df.index[0]}')
    sleep(10)
    # Changing global data doesn't affect the parent process or other processes.
    df[:] = 0
    _g_chunks[chunk_id] = None


if __name__ == '__main__':
    args = parse_args()
    main(args.proc_num, args.no_limits)

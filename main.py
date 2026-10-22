import sys
from collections.abc import Generator, Iterable, Iterator
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from time import perf_counter

from data import LogLevel
from utils import time_spent

VALID_LEVELS = {member.value for member in LogLevel}


def read_file(filename: str) -> Generator[str]:
    with Path(filename).open("r", encoding="utf-8") as f:
        for line in f:
            yield line.rstrip()


@time_spent
def process_lines(lines: Iterator[str], levels: set[str]) -> dict[str, int]:
    result: dict[str, int] = {}
    for line in lines:
        severity = get_severity(line)
        if severity is not None and severity in levels:
            result[severity] = result.get(severity, 0) + 1
    return result


def get_severity(line: str) -> str | None:
    log_array = line.split()
    if len(log_array) > 2:
        log_level = log_array[2]
        return log_level if log_level in VALID_LEVELS else None
    return None


def print_summary(result: dict[str, int]):
    print("Log Analysis Summary")
    print("....................")
    total = 0
    for key, value in result.items():
        total += value
        print(f"{key:<10}{value:>10}")
    print(f"{'TOTAL':<10}{total:>10}")


@time_spent
def process_files(filenames: Iterable[str], levels: set[str]) -> dict[str, int]:
    temp_dict: dict[str, int] = {}
    for filename in filenames:
        result_dict = process_lines(read_file(filename), levels)
        for key in result_dict:
            temp_dict[key] = temp_dict.get(key, 0) + result_dict[key]
    return temp_dict


def process_files_threaded(
    filenames: Iterable[str], levels: set[str]
) -> dict[str, int]:
    with ThreadPoolExecutor(max_workers=3) as executor:
        temp_dict: dict[str, int] = {}
        futures = []
        for filename in filenames:
            future = executor.submit(process_lines, read_file(filename), levels)
            futures.append(future)
        for i, future in enumerate(futures):
            try:
                result_dict = future.result()
                for key in result_dict:
                    temp_dict[key] = temp_dict.get(key, 0) + result_dict[key]
            except FileNotFoundError as err:
                print(f"{i + 1} file does not exit; skipping: {err}")
        return temp_dict


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "app.log"
    levels = {member.value for member in LogLevel}
    if len(sys.argv) > 3:
        levels = {sys.argv[3]} & levels
    # try:
    #     generator = read_file(filename)
    #     print_summary(process_lines(generator, levels))
    # except FileNotFoundError as err:
    #     print(f"File was not found: {err}")
    #     sys.exit(1)
    # print_summary(process_files(["app.log", "database.log", "worker.log"], levels))
    # start = perf_counter()
    # result = process_files_threaded(["large.log", "large2.log", "large3.log"], levels)
    # elapsed = perf_counter() - start

    # print(f"Total threaded time: {elapsed:.6f} seconds")
    # print_summary(result)
    filenames = ["large.log", "large2.log", "large3.log"]
    start = perf_counter()
    result = process_files(filenames, levels)
    elapsed = perf_counter() - start
    print(f"Total sequential time: {elapsed:.6f} seconds")
    print_summary(result)

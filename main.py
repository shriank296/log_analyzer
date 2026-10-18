from collections.abc import Generator, Iterator
from pathlib import Path

from data import LogLevel

VALID_LEVELS = {member.value for member in LogLevel}


def read_file(filename: str) -> Generator[str]:
    with Path(filename).open("r", encoding="utf-8") as f:
        for line in f:
            yield line.rstrip()


def process_lines(lines: Iterator[str]) -> dict[str, int]:
    result: dict[str, int] = {}
    for line in lines:
        severity = get_severity(line)
        if severity is not None:
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


if __name__ == "__main__":
    generator = read_file("app.log")
    print_summary(process_lines(generator))

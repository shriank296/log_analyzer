from collections.abc import Generator, Iterator
from pathlib import Path


def read_file(filename: str) -> Generator[str]:
    with Path(filename).open("r", encoding="utf-8") as f:
        for line in f:
            yield line.rstrip()


def process_lines(lines: Iterator[str]) -> dict[str, int]:
    result: dict[str, int] = {}
    for line in lines:
        severity = get_severity(line)
        result[severity] = result.get(severity, 0) + 1
    return result


def get_severity(line: str) -> str:
    return line.split(" ")[2]


if __name__ == "__main__":
    generator = read_file("app.log")
    print(process_lines(generator))

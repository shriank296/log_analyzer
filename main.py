from collections.abc import Generator
from pathlib import Path


def read_file(filename: str) -> Generator[str]:
    with Path(filename).open("r", encoding="utf-8") as f:
        for line in f:
            yield line.rstrip()


def process_file(filepath: str) -> dict[str, int]:
    result: dict[str, int] = {}
    for line in read_file(filename=filepath):
        severity = get_severity(line)
        if severity in result:
            result[severity] += 1
        else:
            result[severity] = 1
    return result


def get_severity(line: str):
    return line.split(" ")[2]


if __name__ == "__main__":
    output = process_file("app.log")
    print(output)

from collections.abc import Generator
from pathlib import Path

from data import LogLevel


def read_file(filename: str) -> Generator[str]:
    with open(file=filename) as f:
        for line in f:
            yield line.rstrip()


# def process_file(filepath: str):
#     result = {}
#     enum_values = [member.value for member in LogLevel]
#     for line in read_file(filename=filepath):
#         for val in enum_values:
#             if val in line:
#                 if val in result:
#                     result[val] += 1
#                 else:
#                     result[val] = 1
#     return result


def process_file(filepath: str):
    result = {}
    for line in read_file(filename=filepath):
        severity = get_severity(line)
        if severity in result:
            result[severity] += 1
        else:
            result[severity] = 1
    return result


def get_severity(line: str):
    for char in line:
        if char.isalpha():
            start_index = line.index(char)
            i = 0
            severity = ""
            while line[start_index + i] != " ":
                severity += line[start_index + i]
                i += 1
            break
    return severity


if __name__ == "__main__":
    output = process_file("app.log")
    print(output)

import subprocess
import sys
from pathlib import Path

import pytest

from main import get_severity, process_files, process_lines, read_file


@pytest.fixture
def create_temp_file(tmp_path):
    temp_file = Path(tmp_path, "hello.txt")
    temp_file.write_text("Hello world\nThis is new world", encoding="utf-8")
    return temp_file


@pytest.fixture
def create_iterable():
    return [
        "2026-10-17 09:00:08 INFO Order created order_id=1002",
        "2026-10-17 09:00:15 INFO Order processed order_id=1003",
        "2026-10-17 09:00:28 WARNING Retry limit approaching order_id=1002 attempt=",
    ]


@pytest.fixture
def create_line():
    return (
        "2026-10-17 09:00:17 ERROR Payment failed order_id=1002 reason=provider_timeout"
    )


@pytest.fixture
def multiple_log_files(tmp_path):
    temp_files = []
    log_messages = [
        "2026-10-17 09:00:15 INFO Order processed order_id=1003",
        "2026-10-19 09:00:15 ERROR Database query timed out",
        "2026-10-19 10:00:15 WARNING Job 102 is taking longer than expected",
    ]
    for i, log_message in enumerate(log_messages):
        temp_file = Path(tmp_path, f"app.log_{i + 1}")
        temp_file.write_text(log_message)
        temp_files.append(temp_file)
    return temp_files


@pytest.fixture
def multiple_empty_log_files(tmp_path):
    temp_files = []
    log_messages = []
    for i, log_message in enumerate(log_messages):
        temp_file = Path(tmp_path, f"app.log_{i + 1}")
        temp_file.write_text(log_message)
        temp_files.append(temp_file)
    return temp_files


@pytest.fixture
def levels():
    return {"INFO", "DEBUG", "WARNING", "ERROR"}


def test_read_file(create_temp_file):
    generator_file = read_file(create_temp_file)
    assert next(generator_file) == "Hello world"
    assert next(generator_file) == "This is new world"
    with pytest.raises(StopIteration):
        next(generator_file)


def test_process_lines(create_iterable, levels):
    result = process_lines(create_iterable, levels)
    assert isinstance(result, dict)
    assert result["INFO"] == 2


def test_get_severity(create_line):
    assert get_severity(create_line) == "ERROR"


def test_main_execution():
    result = subprocess.run(
        [sys.executable, "main.py"], capture_output=True, text=True, check=True
    )
    assert result.stdout


def test_process_files(multiple_log_files, levels):
    result = process_files(multiple_log_files, levels)
    assert result == {
        "INFO": 1,
        "WARNING": 1,
        "ERROR": 1,
    }


def test_process_empty_files(multiple_empty_log_files, levels):
    result = process_files(multiple_empty_log_files, levels)
    assert result == {}

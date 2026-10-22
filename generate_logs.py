import random
from pathlib import Path


def write_logs() -> None:
    levels = ["INFO", "DEBUG", "WARNING", "ERROR"]
    with Path("large3.log").open("w", encoding="utf-8") as f:
        f.writelines(
            f"2026-10-17 09:00:28 {random.choice(levels)} Retry limit approaching order_id=1002 attempt=3\n"
            for _ in range(100000)
        )


if __name__ == "__main__":
    write_logs()

import random
from pathlib import Path


def write_logs() -> None:
    levels = ["INFO", "DEBUG", "WARNING", "ERROR"]
    with Path("large.log").open("w", encoding="utf-8") as f:
        f.writelines(
            f"2026-10-19 09:00:15 {random.choice(levels)} Order processed order_id=1003\n"
            for _ in range(100000)
        )


if __name__ == "__main__":
    write_logs()

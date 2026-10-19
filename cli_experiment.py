import argparse

parser = argparse.ArgumentParser(description="Analyze application log files.")

parser.add_argument(
    "filename",
    nargs="?",
    default="app.log",
    help="Path to log file (default: app.log)",
)

parser.add_argument(
    "--level", nargs="*", default="ALL", help="Optional level to select"
)

args = parser.parse_args()

print(args.filename)
print(args.level)

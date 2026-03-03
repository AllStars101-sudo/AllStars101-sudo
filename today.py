import re
from datetime import datetime
from dateutil import relativedelta

BIRTHDAY = datetime(2004, 3, 18)


def calculate_uptime() -> str:
    now = datetime.today()
    diff = relativedelta.relativedelta(now, BIRTHDAY)

    parts = []
    if diff.years:
        parts.append(f"{diff.years} year{'s' if diff.years != 1 else ''}")
    if diff.months:
        parts.append(f"{diff.months} month{'s' if diff.months != 1 else ''}")
    if diff.days:
        parts.append(f"{diff.days} day{'s' if diff.days != 1 else ''}")

    return ", ".join(parts) if parts else "0 days"


def update_readme():
    with open("README.md", "r") as f:
        content = f.read()

    uptime = calculate_uptime()

    if not re.search(r'uptime: ".*?"', content):
        print("WARNING: No uptime marker found in README.md")
        return

    updated = re.sub(r'(uptime: ").*?(")', f"\\g<1>{uptime}\\g<2>", content)

    with open("README.md", "w") as f:
        f.write(updated)
    print(f"Uptime: {uptime}")


if __name__ == "__main__":
    update_readme()

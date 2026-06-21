import random

from random import choice, randint
from string import ascii_letters, digits
from datetime import datetime, timedelta, timezone


def random_string(start: int = 9, end: int = 15) -> str:
    return "".join(choice(ascii_letters + digits) for _ in range(randint(start, end)))


def random_list_of_strings(start: int = 9, end: int = 15) -> list[str]:
    return [random_string() for _ in range(randint(start, end))]


def generate_random_date_within_year() -> str:
    today = datetime.now()
    start_date = today - timedelta(days=365)
    end_date = today
    random_date = start_date + timedelta(
        seconds=random.randint(0, int((end_date - start_date).total_seconds()))
    )
    return random_date.isoformat()


def generate_random_time_data(num_samples=5):
    data = []
    for _ in range(num_samples):
        start_datetime = datetime.now(tz=timezone.utc) - timedelta(
            days=random.randint(0, 365)
        )
        time_delta = timedelta(
            hours=random.randint(0, 48), minutes=random.randint(0, 59)
        )
        end_datetime = start_datetime + time_delta
        start_iso = start_datetime.isoformat()
        end_iso = end_datetime.isoformat()

        expected_difference_hours = int(time_delta.total_seconds() // 3600)

        data.append((start_iso, end_iso, expected_difference_hours))
    return data


def generator_datatime_format():
    start_datetime = datetime.now(tz=timezone.utc)
    end_datetime = start_datetime + timedelta(days=365)
    random_datetime = start_datetime + (end_datetime - start_datetime) * random.random()
    return random_datetime.strftime("%Y-%m-%dT%H:%M:%S")

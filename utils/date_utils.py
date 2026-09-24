from datetime import date, datetime, timedelta


def today_str() -> str:
    return date.today().isoformat()


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def date_range(days: int) -> list[str]:
    end = date.today()
    return [(end - timedelta(days=i)).isoformat() for i in range(days - 1, -1, -1)]


from datetime import date


def parse_due_date(raw_due_date):
    if not raw_due_date:
        return None
    try:
        return date.fromisoformat(raw_due_date)
    except ValueError:
        return None

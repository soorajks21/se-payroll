from datetime import date
from typing import Tuple

def get_pay_period(date: date) -> Tuple[date, date]:
    if date.day <= 15:
        start_date = date.replace(day=1)
        end_date = date.replace(day=15)
    else:
        start_date = date.replace(day=16)
        end_date = date.replace(day=date.day)
    return start_date, end_date

def calculate_amount_paid(hours_worked: float, job_group: str) -> float:
    if job_group == 'A':
        return hours_worked * 20
    elif job_group == 'B':
        return hours_worked * 30
    return 0.0
from pydantic import BaseModel
from datetime import date
from typing import List

class PayPeriod(BaseModel):
    startDate: date
    endDate: date

class EmployeeReport(BaseModel):
    employeeId: str
    payPeriod: PayPeriod
    amountPaid: str

class PayrollReport(BaseModel):
    employeeReports: List[EmployeeReport]
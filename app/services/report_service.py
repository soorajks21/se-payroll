from collections import defaultdict
from sqlalchemy.orm import Session
from app.crud import time_report
from app.schemas.report import PayrollReport, EmployeeReport, PayPeriod
from app.utils.date_utils import get_pay_period, calculate_amount_paid

class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def generate_payroll_report(self) -> PayrollReport:
        reports = time_report.get_all(self.db)
        employee_reports = defaultdict(lambda: defaultdict(float))

        for report in reports:
            start_date, end_date = get_pay_period(report.date)
            key = (report.employee_id, start_date, end_date)
            employee_reports[key]['hours_worked'] += report.hours_worked
            employee_reports[key]['job_group'] = report.job_group

        payroll_report = []
        for (employee_id, start_date, end_date), data in employee_reports.items():
            amount_paid = calculate_amount_paid(data['hours_worked'], data['job_group'])
            payroll_report.append(EmployeeReport(
                employeeId=employee_id,
                payPeriod=PayPeriod(startDate=start_date, endDate=end_date),
                amountPaid=f"${amount_paid:.2f}"
            ))

        return PayrollReport(employeeReports=sorted(payroll_report, key=lambda x: (x.employeeId, x.payPeriod.startDate)))
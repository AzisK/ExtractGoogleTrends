import pendulum

def get_date_from_airflow(context):
    return context['logical_date']

class Date:
    date = pendulum.now().subtract(days=1)
    passed_date = None

    def pass_date(self, passed_date):
        self.passed_date = passed_date
        if passed_date:
            self.date = passed_date
        if self.date.to_date_string() == pendulum.now().to_date_string():
            self.date = passed_date.subtract(days=1)
        return self

    @property
    def date_str(self):
        return self.date.to_date_string()

    @property
    def date_param(self):
        start_date = self.date.subtract(days=0)
        return f"{start_date:%Y-%m-%d} {self.date:%Y-%m-%d}"

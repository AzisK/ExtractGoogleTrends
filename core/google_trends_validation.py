from pydantic import BaseModel

from core.date import Date
from core.params import Params

DEFAULT_SEARCH_PARAMETERS = {
    "engine": "google_trends",
    "q": "vpn,antivirus,ad blocker,password manager",
    "hl": "en",
    "geo": "US",
    "tz": "420",
    "data_type": "TIMESERIES"
}

class Query(BaseModel):
    query: str
    value: str
    extracted_value: int

class GoogleTrendsResultsValidator(Date, Params):
    def __init__(self, results):
        self.results = results

    def validate(self):
        self.validate_is_full_data()

        self.validate_search_parameters()

        self.validate_date_count()

        self.validate_day()

        self.validate_queries()

        self.validate_data_types()

    def validate_is_full_data(self):
        timeline_data = self.results['interest_over_time']['timeline_data'][0]
        if 'partial_data' in timeline_data:
            assert not timeline_data['partial_data'] == True, "Response seems to give us partial data"

    def validate_search_parameters(self):
        params_expected = {**DEFAULT_SEARCH_PARAMETERS, **self.params, **{'date': self.date_param}}
        params_got = self.results['search_parameters']
        assert params_got == params_expected \
            , f"Search parameters do not match. Expected:\n{params_expected}\nGot:\n{params_got}"

    def validate_date_count(self):
        days_expected = 1
        days_got = len(self.results['interest_over_time']['timeline_data'])
        assert len(self.results['interest_over_time']['timeline_data']) == days_expected \
            , f"Expected {days_expected} days, got {days_got} days"

    def validate_day(self):
        timeline_day_expected = f"{self.date:MMM D, YYYY}"
        timeline_day_got = self.results['interest_over_time']['timeline_data'][0]['date']
        assert timeline_day_expected == timeline_day_got \
            , f"Expected timeline day {timeline_day_expected}, got {timeline_day_got}"

    def validate_queries(self):
        queries_expected = self.params['q'].split(',')
        values = self.results['interest_over_time']['timeline_data'][0]['values']
        queries_got = [q['query'] for q in values]
        assert queries_expected == queries_got \
            , f"Expected queries {queries_expected}, got {queries_got}"

    def validate_data_types(self):
        for q in self.results['interest_over_time']['timeline_data'][0]['values']:
            Query.model_validate(q)

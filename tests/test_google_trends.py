import unittest
from copy import deepcopy

import pandas as pd
import pendulum
from pandas.testing import assert_frame_equal
from pydantic import ValidationError as PydanticValidationError

from core.google_trends import GoogleTrends
from core.google_trends_validation import GoogleTrendsResultsValidator
from tests.consants import SAMPLE_RESPONSE, SAMPLE_DATE, SAMPLE_TRANSFORMED_RESPONSE, SAMPLE_BAD_RESPONSE, \
    SAMPLE_PARAMS_DIFFERENT, SAMPLE_RESPONSE_DIFFERENT


class TestGoogleTrendsTransformation(unittest.TestCase):
    def setUp(self):
        self.test_date = pendulum.parse(SAMPLE_DATE)
        self.google_trends = GoogleTrends().pass_date(self.test_date)
        self.test_data = SAMPLE_RESPONSE

    def test_transform(self):
        sample_df = pd.json_normalize(SAMPLE_TRANSFORMED_RESPONSE)
        sample_df.rename(columns={'extracted_value': 'cnt'}, inplace=True)
        sample_df.insert(0, 'date', self.google_trends.date_str)

        assert_frame_equal(
            self.google_trends.transform(self.test_data)[['date', 'query', 'cnt']],
            sample_df
        )


class TestGoogleTrendsValidation(unittest.TestCase):
    def setUp(self):
        self.test_date = pendulum.parse(SAMPLE_DATE)

    def test_successful(self):
        validator = GoogleTrendsResultsValidator(SAMPLE_RESPONSE).pass_date(self.test_date)
        validator.validate()

    def test_partial_data(self):
        invalid_response = deepcopy(SAMPLE_RESPONSE)
        invalid_response['interest_over_time']['timeline_data'][0]['partial_data'] = True

        validator = GoogleTrendsResultsValidator(invalid_response).pass_date(self.test_date)
        with self.assertRaises(AssertionError) as context:
            validator.validate()
        self.assertIn("partial data", str(context.exception))

    def test_search_parameters(self):
        invalid_response = deepcopy(SAMPLE_RESPONSE)
        invalid_response['search_parameters']['geo'] = 'ES'

        validator = GoogleTrendsResultsValidator(invalid_response).pass_date(self.test_date)
        with self.assertRaises(AssertionError) as context:
            validator.validate()
        self.assertIn("Search parameters do not match", str(context.exception))

    def test_date_count(self):
        invalid_response = deepcopy(SAMPLE_RESPONSE)
        invalid_response['interest_over_time']['timeline_data'] = [
            invalid_response['interest_over_time']['timeline_data'][0],
            invalid_response['interest_over_time']['timeline_data'][0]
        ]

        validator = GoogleTrendsResultsValidator(invalid_response).pass_date(self.test_date)
        with self.assertRaises(AssertionError) as context:
            validator.validate()
        self.assertIn("Expected 1 days", str(context.exception))

    def test_wrong_day(self):
        invalid_response = deepcopy(SAMPLE_RESPONSE)
        invalid_response['interest_over_time']['timeline_data'][0]['date'] = "May 3, 2025"

        validator = GoogleTrendsResultsValidator(invalid_response).pass_date(self.test_date)
        with self.assertRaises(AssertionError) as context:
            validator.validate()
        self.assertIn("Expected timeline day", str(context.exception))

    def test_wrong_queries(self):
        invalid_response = deepcopy(SAMPLE_RESPONSE)
        invalid_response['interest_over_time']['timeline_data'][0]['values'][0][
            'query'] = "firewall"  # Changed from vpn

        validator = GoogleTrendsResultsValidator(invalid_response).pass_date(self.test_date)
        with self.assertRaises(AssertionError) as context:
            validator.validate()
        self.assertIn("Expected queries", str(context.exception))

    def test_null_query_counts(self):
        invalid_response = deepcopy(SAMPLE_BAD_RESPONSE)
        validator = GoogleTrendsResultsValidator(invalid_response).pass_date(self.test_date)
        with self.assertRaises(PydanticValidationError) as context:
            validator.validate()
        self.assertIn("Input should be a valid integer", str(context.exception))

    def test_different_params(self):
        response = deepcopy(SAMPLE_RESPONSE_DIFFERENT)
        validator = GoogleTrendsResultsValidator(response).pass_params(**SAMPLE_PARAMS_DIFFERENT).pass_date(self.test_date)
        validator.validate()

if __name__ == '__main__':
    unittest.main()

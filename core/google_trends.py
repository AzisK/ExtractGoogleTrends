import json
import os
import sys
from pathlib import Path

import duckdb
import pandas as pd
import pendulum
import requests.exceptions
import serpapi
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

sys.path.append(str(Path(__file__).parent.parent))
from core.date import Date
from core.google_trends_validation import GoogleTrendsResultsValidator
from core.params import Params

load_dotenv()
api_key = os.getenv('SERPAPI_KEY')
client = serpapi.Client(api_key=api_key)
DB_DIR = Path(__file__).parent.parent / 'db'
DB_PATH = DB_DIR / 'google_trends.db'
DB_TABLE = 'google_trends'

class GoogleTrends(Date, Params):
    engine = "google_trends"

    @property
    def client(self):
        return client

    def extract(self):
        params = {**self.params, **{"date": self.date_param}, **{"engine": self.engine}}

        @retry(
            stop=stop_after_attempt(5),
            wait=wait_exponential(multiplier=1, min=2, max=60),
            retry=retry_if_exception_type((
                    requests.exceptions.Timeout,
                    serpapi.HTTPError,
                    serpapi.HTTPConnectionError,
            ))
        )
        def _execute_search_with_retry():
            try:
                search = client.search(**params)
                return search.as_dict()
            except Exception as e:
                print(f"API request failed: {str(e)}. Retrying...")
                raise

        print(f"Searching Google Trends for date: {self.date_str}")
        results = _execute_search_with_retry()
        return results

    def extract_and_save(self):
        results = self.extract()
        self.save_json(results)

    @property
    def file_json(self):
        return f"/tmp/google_trends_{self.date_str}.json"

    @property
    def file_csv(self):
        return f"/tmp/google_trends_{self.date_str}.csv"

    def save_json(self, json_data):
        with open(self.file_json, "w") as f:
            print(f"Saving json to {self.file_json}")
            json.dump(json_data, f, indent=2)

    def read_json(self):
        with open(self.file_json, "r") as f:
            data = json.load(f)
        return data

    def validate(self, results):
        GoogleTrendsResultsValidator(results).pass_params(**self.passed_params).pass_date(self.passed_date).validate()

    def transform(self, results):
        queries = results['interest_over_time']['timeline_data'][0]['values']
        created_timestamp = pendulum.now().format('YYYY-MM-DD HH:mm:ss')
        relevant_data = [
            {
                'date': self.date_str,
                'query': q['query'],
                'cnt': q['extracted_value'],
                'created_timestamp': created_timestamp,
                'modified_timestamp': created_timestamp,
            }
            for q in queries]
        df = pd.json_normalize(relevant_data)
        return df

    def transform_and_save(self, results):
        df = self.transform(results)
        print(f"Saving CSV to {self.file_csv}")
        df.to_csv(self.file_csv, index=False)

    def load(self):
        with duckdb.connect(DB_PATH) as conn:
            exists = conn.execute(f"SELECT COUNT(*) FROM {DB_TABLE} WHERE datestamp = '{self.date_str}'").fetchone()[0] > 0
            if exists:
                print(f"Data found for {self.date_str}. Deleting existing records...")
                conn.execute(f"DELETE FROM {DB_TABLE} WHERE datestamp = '{self.date_str}'")
                print(f"Deleted existing data for {self.date_str}")

            print(f"Loading data from {self.file_csv} to {DB_PATH} to table {DB_TABLE} for {self.date_str}")
            results = conn.execute(f"COPY {DB_TABLE} FROM '{self.file_csv}' (AUTO_DETECT TRUE)")
            print(f"Data loaded successfully: {results}")


def run():
    google_trends_object = GoogleTrends()
    google_trends_object.extract_and_save()
    r = google_trends_object.read_json()
    google_trends_object.validate(r)
    google_trends_object.transform_and_save(r)
    google_trends_object.load()

if __name__ == "__main__":
    run()

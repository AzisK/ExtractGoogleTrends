import sys
from pathlib import Path

import pendulum
from airflow.sdk import dag, task

sys.path.append(str(Path(__file__).parent.parent))
from core.date import get_date_from_airflow
from core.google_trends import GoogleTrends
from airflow.models import Variable

geo = Variable.get("google_trends_geo", default_var=None)
q = Variable.get("google_trends_q", default_var=None)
google_trends_object = GoogleTrends().pass_params(geo, q)

@dag(
    schedule='@daily',
    start_date=pendulum.datetime(2025, 5, 8, tz="UTC"),
    catchup=True,
    tags=["google"],
)
def google_trends():
    @task
    def extract(**context):
        date = get_date_from_airflow(context)
        google_trends_object.pass_date(date).extract_and_save()

    @task
    def transform(**context):
        date = get_date_from_airflow(context)
        results = google_trends_object.pass_date(date).read_json()
        google_trends_object.validate(results)
        google_trends_object.transform_and_save(results)

    @task
    def load(**context):
        date = get_date_from_airflow(context)
        google_trends_object.pass_date(date).load()

    extract() >> transform() >> load()

google_trends()

# Extract Google Trends using SerpApi and Airflow

This project is a simple example of how to extract Google Trends data using SerpApi and Apache Airflow. It demonstrates how to set up a DAG (Directed Acyclic Graph) in Airflow to automate the process of fetching and storing Google Trends data inside DuckDB locally.

The job can be run via Airflow or simply via terminal

```bash
python google_trends.py
```

The code has been tested with Python 3.12 and Airflow 3.0.0. Feel free to use other versions of Python and Airflow but keep in mind that it has not been tested.

Airflow can be run with this script

```bash
airflow standalone
```

## A. Installation

1. Initialize virtual environment

One of the way to do it, though there are many 

```bash
python3.12 -m venv .venv
```

2. Activate virtual environment

```bash
source .venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Get SerpApi API key

You need to get the SerpApi key from https://serpapi.com/. Register and generate a key. It gives you 100 free searches per month.

Put the key in the `.env` file in the root directory of the project. The key in the file should look like this:

```bash
SERPAPI_KEY=<123_YOURKEY_ABC>
```

5. DuckDB database preparation

Run the Python script in `db/migrate.py` to create a DuckDB database file called `db/google_trends.db` together with a table described in `db/create_table.sql`.

Keep in mind that this database is not concurrent and does not support multiple connections.

6. Configure Airflow

Configure your Airflow home directory. You can do it by setting the `AIRFLOW_HOME` environment variable. The default value is `~/airflow`. You can change it to any other directory you want.

For example, it can be set in ~/.zprofile or ~/.bash_profile

```bash
export AIRFLOW_HOME=~/airflow
```

This will create an `airflow.cfg` file in the `~/airflow` directory once you run it.

Once this is done, you need to set the `jwt_secret` inside you `airflow.cfg`. Set it under `[api_auth]` section. It should look like this:

```bash
[api_auth]
jwt_secret = <your_jwt_secret>
```

## Pipeline design

This is a very simple approach to the pipeline. It has been designed to work with or without Airflow.

Core of the logic of the pipeline is in `core/google_trends.py` file. It contains a class `GoogleTrends` that is responsible for fetching the data from SerpApi, validating it, transforming and storing it in DuckDB.

Locally, it could be run and debugged as in the `run` function inside the file:

```python
def run():
    google_trends_object = GoogleTrends()
    google_trends_object.extract_and_save()
    r = google_trends_object.read_json()
    google_trends_object.validate(r)
    google_trends_object.transform_and_save(r)
    google_trends_object.load()
```

The methods of the class are divided so, that they could be easily transferred to Airflow tasks.

The Airflow DAG using the TaskFlowAPI looks like this while using the methods of the class. The class is there for general configuration and coordination of the variables.

```python
def google_trends():
    @task
    def extract(**context):
        date = get_date_from_airflow(context)
        results = google_trends_object.pass_date(date).extract_and_save()
        return results

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
```

The tasks in Airflow use local disk space files to pass data between each other. When running the methods of the `GoogleTrends` object, they also use the local disk space files to pass data between each other. The files are stored in the `/tmp` directory.

The pipeline is not using the Airflow XCom feature to pass data between tasks on purpose since we want the script to be able to run without Airflow as well.

## How to extend the pipeline?

The pipeline can be extended in a similar way as it is done in the `core/google_trends.py` file. You can add new methods to the class and call them in the Airflow DAG. 

You also avoid this class and use another one and avoid classes in general if that is convenient to you.

Different DAGs can be created in a similar manner as well.

## How can this pipeline be scaled?

First of all, we can upgrade the databases.

We can upgrade our DuckDB file and use a proper database or a datalake that supports concurrent connections.

We can also upgrade the Airflow database and use MySQL or PostgreSQL instead of SQLite.

Then we also need to move from development Airflow to production Airflow. 

If we run our workers on different machines, then we also need to move from the local storage to something globally available. For small data transfers we could use Airflow's XCom but that would make the script not runnable locally without Airflow.

Then we could exchange data between tasks using a datalake like S3 or similar.

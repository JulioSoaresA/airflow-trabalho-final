import sys
sys.path.append("airflow_pipeline")

from airflow.models import DAG
from datetime import datetime, timedelta
from operators.twitter_operator import TwitterOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

from os.path import join
from airflow.utils.dates import days_ago
from pathlib import Path

with DAG(dag_id = "TwitterDAG", start_date=days_ago(6), schedule_interval="@daily") as dag:
    BASE_FOLDER = join(
       str(Path("~/Projects/EGD").expanduser()),
       "airflow-trabalho-final/datalake/{stage}/twitter_datascience/{partition}",
   )
    PARTITION_FOLDER_EXTRACT = "extract_date={{ data_interval_start.strftime('%Y-%m-%d') }}"
    TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.00Z"
    query = "datascience"

    twitter_operator = TwitterOperator(file_path=join(BASE_FOLDER.format(stage="Bronze", partition=PARTITION_FOLDER_EXTRACT),
                                        "datascience_{{ ds_nodash }}.json"),
                                        query=query,
                                        start_time="{{ data_interval_start.strftime('%Y-%m-%dT%H:%M:%S.00Z') }}",
                                        end_time="{{ data_interval_end.strftime('%Y-%m-%dT%H:%M:%S.00Z') }}",
                                        task_id="twitter_datascience")

    twitter_transform = SparkSubmitOperator(task_id="transform_twitter_datascience",
                                            application="/home/julioubuntu/Projects/EGD/airflow-trabalho-final/src/spark/transformation.py",
                                            name="twitter_transformation",
                                            application_args=["--src", BASE_FOLDER.format(stage="Bronze", partition=PARTITION_FOLDER_EXTRACT),
                                             "--dest", BASE_FOLDER.format(stage="Silver", partition=""),
                                             "--process-date", "{{ data_interval_start.strftime('%Y-%m-%d') }}"])

    twitter_insight = SparkSubmitOperator(task_id="insight_twitter",
                                            application="/home/julioubuntu/Projects/EGD/airflow-trabalho-final/src/spark/insight_tweet.py",
                                            name="insight_twitter",
                                            application_args=["--src", BASE_FOLDER.format(stage="Silver", partition=""),
                                             "--dest", BASE_FOLDER.format(stage="Gold", partition=""),
                                             "--process-date", "{{ data_interval_start.strftime('%Y-%m-%d') }}"])

twitter_operator >> twitter_transform >> twitter_insight
    
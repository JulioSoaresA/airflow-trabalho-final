from datetime import datetime
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator


with DAG(dag_id="GoldLayerDAG", start_date=datetime(2023, 12, 14), schedule_interval="@once") as dag:

    create_gold_table_query = """
    CREATE TABLE IF NOT EXISTS gold_layer_table (
        id SERIAL PRIMARY KEY,
        folder_name VARCHAR(255),
        refinement_date TIMESTAMP,
        file_name VARCHAR(255),
        file_data JSONB
    );
    """

    create_gold_table_task = PostgresOperator(
        task_id='create_gold_table',
        sql=create_gold_table_query,
        postgres_conn_id='postgres_default',
    )


create_gold_table_task
from datetime import datetime
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator


with DAG(dag_id="DropGoldLayerDAG", start_date=datetime(2023, 12, 14), schedule_interval="@once") as dag:

    drop_gold_table_query = """
    DROP TABLE gold_layer_table;
    """

    drop_gold_table_task = PostgresOperator(
        task_id='drop_gold_table',
        sql=drop_gold_table_query,
        postgres_conn_id='postgres_default',
    )


drop_gold_table_task
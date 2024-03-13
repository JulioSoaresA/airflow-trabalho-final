import logging
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from pymongo import MongoClient
import os
from os.path import join
from pathlib import Path

# Configurações do MongoDB Atlas
MONGO_URI = "mongodb+srv://juliosoares063:engdados@cluster0.n77ab7r.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "airflow"
COLLECTION_NAME = "airflow_mongo"

# Função para armazenar a pasta de arquivos JSON no MongoDB
def store_folder_in_mongo(folder_path, medalha):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file:
                    json_data = file.read()
                    api_nome = os.path.basename(os.path.dirname(os.path.dirname(file_path)))
                    extracao_nome = os.path.basename(os.path.dirname(file_path))
                    data = {
                        "timestamp": datetime.utcnow(),
                        "json_data": json_data,
                        "file_name": file_name,
                        "medalha": medalha,
                        "api_nome": api_nome,
                        "extracao_nome": extracao_nome
                    }
                    logging.info(f"Inserting {file_name} into MongoDB teste")
                    logging.info(f"Inserting {json_data} into MongoDB")
                    logging.info(f"Inserting {file_name} into MongoDB")
                    logging.info(f"Inserting {medalha} into MongoDB")
                    logging.info(f"Inserting {api_nome} into MongoDB")
                    logging.info(f"Inserting {extracao_nome} into MongoDB")
                    # collection.insert_one(data)

    client.close()


with DAG(dag_id = "ArmazenaPastaMongoDBDAG", start_date = datetime(2023, 1, 1), schedule_interval="@daily") as dag:
    BASE_FOLDER = join(
        str(Path("~/Projects/EGD").expanduser()),
        "airflow-trabalho-final/datalake/{stage}/",
    )

    task_store_folder = PythonOperator(
        task_id='store_folder',
        python_callable=store_folder_in_mongo,
        op_args=[BASE_FOLDER.format(stage='Gold'), 'Gold'],  # Substitua pelo caminho real da sua pasta
    )

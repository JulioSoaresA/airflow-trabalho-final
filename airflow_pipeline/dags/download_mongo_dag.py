from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from pymongo import MongoClient
import os

# Configurações do MongoDB Atlas
MONGO_URI = "mongodb+srv://juliosoares063:engdados@cluster0.n77ab7r.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "airflow"
COLLECTION_NAME = "airflow_mongo"
LOCAL_OUTPUT_PATH = "/home/julioubuntu/Projects/EGD/airflow-trabalho-final/datalake/Gold/MongoDB"

# Função para recuperar dados do MongoDB e salvar localmente
def retrieve_and_save_data_locally():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Consulta para obter os dados desejados (substitua conforme necessário)
    query = {}
    cursor = collection.find(query)

    # Itera sobre os documentos retornados
    for document in cursor:
        file_name = document.get("file_name")
        json_data = document.get("json_data")

        # Cria o caminho local onde os dados serão salvos
        local_file_path = os.path.join(LOCAL_OUTPUT_PATH, file_name)

        # Salva os dados localmente
        with open(local_file_path, 'w') as local_file:
            local_file.write(json_data)

    client.close()


with DAG(dag_id = "DownloadMongoDBDAG", start_date = datetime(2023, 1, 1), schedule_interval="@daily") as dag:

    task_retrieve_and_save = PythonOperator(
        task_id='retrieve_and_save',
        python_callable=retrieve_and_save_data_locally,
    )

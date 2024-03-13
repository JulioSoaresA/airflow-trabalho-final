# Criação de pipelines de processamento de dados utilizando Apache Spark e Apache Airflow

## Objetivo
Desenvolver pipelines de processamento de dados em tempo real por meio da criação de aplicações
Apache Spark Streaming, que serão responsáveis pelo consumo de dados a partir de um Data Lake. Utilizando
a ferramenta Apache Airflow, o objetivo é agendar, orquestrar e monitorar de maneira eficiente os fluxos de
processamento de dados, garantindo a escalabilidade e confiabilidade das operações ETL, com foco na
análise e transformação de dados em tempo real.

## Estrutura do projeto
O projeto está organizado da seguinte maneira:

- airflow_pipeline/: Contém tudo relacionado ao airflow como DAGs (Directed Acyclic Graphs), Hooks, Logs, Operators e os arquivos de configuração do airflow que definem os fluxos de trabalho.
- datalake/: É onde são armazenados os dados extraidos
    - Bronze/: São arquivos brutos sem nenhuma transformação.
    - Silver/: São arquivos um pouco mais tratados onde são separados dados considerados importantes.
    - Gold/: São arquivos refinados com apenas dados que serão usados.
src/: É a pasta onde são guardados os notebooks usados para observar os dados, scripts usados e arquivos executáveis do spark.

## Configuração
1. Ambiente Virtual:
    Crie um ambiente virtual para isolar as dependências do projeto:
    ```bash
        python -m venv venv
        source venv/bin/activate
    ```

2. Instalação das Dependências:
    Instale as dependências do projeto:
    ```bash
        pip install -r requirements.txt
    ```

3. Instalação e extração do spark-hadoop:
    ```bash
        wget https://archive.apache.org/dist/spark/spark-3.1.3/spark-3.1.3-bin-hadoop3.2.tgz
    ```
    ```bash
        tar -xvzf spark-3.1.3-bin-hadoop3.2.tgz
    ```

4. Configuração do Apache Airflow:
    Configure o Apache Airflow de acordo com as necessidades do projeto. Certifique-se de configurar as variáveis de ambiente e o arquivo de configuração airflow.cfg adequadamente.
    ```bash
        export AIRFLOW_HOME=$(pwd)/airflow_pipeline
    ```

5. Definindo a variável de ambiente do spark:
    ```bash
        export SPARK_HOME=$(pwd)/spark-3.1.3-bin-hadoop3.2
    ```    

6. Rodar o airflow:
    ```bash
        airflow standalone
    ```
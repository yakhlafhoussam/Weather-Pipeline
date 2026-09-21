from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from extraction.bronze import run_bronze
from transformation.silver import run_silver
from transformation.gold import run_gold
from load.load import save_data


origine = "sources/ma.csv"

bronze = "data/bronze"
silver = "data/silver"
gold = "data/gold"


def bronze_task():
    run_bronze(origine, bronze)


def silver_task():
    run_silver(
        f"{bronze}/weather/weather.json",
        f"{silver}/weather_clean.csv"
    )


def gold_task():
    run_gold(
        f"{silver}/weather_clean.csv",
        f"{gold}/weather_gold.csv"
    )


def load_task():
    save_data()


with DAG(
    dag_id="weather_pipeline",
    start_date=datetime(2026, 9, 20),
    schedule="@daily",
    catchup=False,
) as dag:

    bronze_task_operator = PythonOperator(
        task_id="bronze",
        python_callable=bronze_task
    )

    silver_task_operator = PythonOperator(
        task_id="silver",
        python_callable=silver_task
    )

    gold_task_operator = PythonOperator(
        task_id="gold",
        python_callable=gold_task
    )

    load_task_operator = PythonOperator(
        task_id="load",
        python_callable=load_task
    )

bronze_task_operator >> silver_task_operator >> gold_task_operator >> load_task_operator
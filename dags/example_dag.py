from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

dag = DAG(
    dag_id='example_dag',
    description='Contoh DAG sederhana',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

task_1 = PythonOperator(
    task_id='say_hello',
    python_callable=lambda: print("Hello, Airflow!"),
    dag=dag,
)

task_2 = PythonOperator(
    task_id='say_goodbye',
    python_callable=lambda: print("Goodbye, Airflow!"),
    dag=dag,
)

task_1 >> task_2
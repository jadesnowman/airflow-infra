from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import feedparser

def fetch_feed():
    url = "https://techcrunch.com/feed"
    feed = feedparser.parse(url)
    for item in feed.entries:
        categories = [tag.term for tag in item.tags]

# Define the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 1),
    'retries': 1,
}

dag = DAG(
    'fetch_feed_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
)

fetch_task = PythonOperator(
    task_id='fetch_feed_task',
    python_callable=fetch_feed,
    dag=dag
)

fetch_task

from airflow import DAG
from airflow.operators.python import PythonOperator
# from airflow.hooks.base import BaseHook
# from pymongo import MongoClient
from datetime import datetime, timedelta
import feedparser
import logging

# Define default_args for DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 1),
    "retries": 2,  # Retries on failure
    "retry_delay": timedelta(minutes=5),
}

# # MongoDB Connection
# def get_mongo_client():
#     conn = BaseHook.get_connection("mongo_default")  # Airflow Connection
#     mongo_uri = f"mongodb://{conn.host}:{conn.port}/"
#     return MongoClient(mongo_uri)[conn.schema]

# Extract: Scrape RSS Feed
def scrape_rss(**kwargs):
    feed = feedparser.parse("https://techcrunch.com/feed")

    if not feed.entries:
        logging.warning("No RSS entries found.")
        return []

    articles = []
    for entry in feed.entries:
        print(entry)
        article = {
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "categories": [tag.term for tag in entry.tags] if hasattr(entry, "tags") else [],
        }
        articles.append(article)

    logging.info(f"Scraped {len(articles)} articles.")
    return articles

def store_to_mongodb(**kwargs):
    ti = kwargs["ti"]
    articles = ti.xcom_pull(task_ids="scrape_rss_feed")

    if not articles:
        logging.warning("No articles to insert.")
        return

    # db = get_mongo_client()
    # collection = db["rss_feeds"]

    # for article in articles:
    #     collection.update_one(
    #         {"link": article["link"]},  # Avoid duplicates by link
    #         {"$set": article},
    #         upsert=True,
    #     )

    logging.info(f"Inserted {len(articles)} articles into MongoDB.")
    ti.xcom_clear()

dag = DAG(
    'feed_dag',
    default_args=default_args,
    schedule_interval='@hourly',
    catchup=False
)

scrape_task = PythonOperator(
    task_id='scrape_rss_feed',
    python_callable=scrape_rss,
    dag=dag
)

store_task = PythonOperator(
    task_id='store_to_mongodb',
    python_callable=store_to_mongodb,
    dag=dag
)

scrape_task >> store_task

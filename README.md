docker compose down --volumes --remove-orphans

airflow tasks test fetch_feed_dag fetch_feed_task $(date -I)

airflow dags list
airflow tasks list feed_dag

airflow tasks test feed_dag scrape_rss_feed $(date -I)

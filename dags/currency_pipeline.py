from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from scripts.extract_currency import extract_currency
from scripts.transform_currency import transform_currency
from scripts.load_currency import load_currency

from scripts.transform_gold import transform_gold
from scripts.load_gold import load_gold

from scripts.extract_bps_neraca import extract_exportimport
from scripts.transform_exportimport import transform_exportimport
from scripts.load_exportimport import load_exportimport

from scripts.extract_usd_index import extract_usd_index
from scripts.transform_usd_index import transform_usd_index
from scripts.load_usd_index import load_usd_index

from scripts.extract_ihsg import extract_ihsg
from scripts.transform_ihsg import transform_ihsg
from scripts.load_ihsg import load_ihsg

with DAG(
    dag_id="currency_daily_rates",
    start_date=datetime(2026, 1, 1),
    schedule="0 8 * * *",
    catchup=False,
    tags=["currency", "api"],
) as dag:

    extract = PythonOperator(
        task_id="extract_currency",
        python_callable=extract_currency,
    )

    # =========================
    # CURRENCY
    # =========================

    transform = PythonOperator(
        task_id="transform_currency",
        python_callable=transform_currency,
    )

    load = PythonOperator(
        task_id="load_currency_postgres",
        python_callable=load_currency,
    )

    # =========================
    # GOLD
    # =========================

    transform_gold_task = PythonOperator(
        task_id="transform_gold",
        python_callable=transform_gold,
    )

    load_gold_task = PythonOperator(
        task_id="load_gold_postgres",
        python_callable=load_gold,
    )

    # =========================
    # EXPORT - IMPORT BPS
    # =========================

    extract_exportimport_task = PythonOperator(
        task_id="extract_exportimport",
        python_callable=extract_exportimport,
    )

    transform_exportimport_task = PythonOperator(
        task_id="transform_exportimport",
        python_callable=transform_exportimport,
    )

    load_exportimport_task = PythonOperator(
        task_id="load_exportimport_postgres",
        python_callable=load_exportimport,
    )

    # =========================
    # USD INDEX
    # =========================

    extract_usd_index_task = PythonOperator(
        task_id="extract_usd_index",
        python_callable=extract_usd_index,
    )

    transform_usd_index_task = PythonOperator(
        task_id="transform_usd_index",
        python_callable=transform_usd_index,
    )

    load_usd_index_task = PythonOperator(
        task_id="load_usd_index_postgres",
        python_callable=load_usd_index,
    )

    # =========================
    # IHSG
    # =========================

    extract_ihsg_task = PythonOperator(
        task_id="extract_ihsg",
        python_callable=extract_ihsg,
    )

    transform_ihsg_task = PythonOperator(
        task_id="transform_ihsg",
        python_callable=transform_ihsg,
    )

    load_ihsg_task = PythonOperator(
        task_id="load_ihsg_postgres",
        python_callable=load_ihsg,
    )

    # =========================
    # ALUR TASK
    # =========================

    extract >> transform >> load
    extract >> transform_gold_task >> load_gold_task
    extract_exportimport_task >> transform_exportimport_task >> load_exportimport_task
    extract_usd_index_task >> transform_usd_index_task >> load_usd_index_task
    extract_ihsg_task >> transform_ihsg_task >> load_ihsg_task
from airflow.decorators import dag
from datetime import datetime
from default.tasks import imprimir

@dag(
    dag_id="exemplo-print",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["exemplo"],
)
def exemplo_dag():
    imprimir()

dag_instancia = exemplo_dag()

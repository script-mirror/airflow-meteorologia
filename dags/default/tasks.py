from airflow.decorators import task

@task
def imprimir():
    print("Hello Airflow 3")
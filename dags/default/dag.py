from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from airflow.providers.ssh.operators.ssh import SSHOperator
import datetime

TIME_OUT = 60*60*30
SSH = "ssh -i /opt/airflow/config/chave-middle.pem -o StrictHostKeyChecking=no admin@tradingenergiarz.com"
 
def create_model_dag(model_name, schedule):

    @dag(
        dag_id=f"{model_name.upper()}",
        start_date=datetime.datetime(2025, 1, 1),
        schedule=schedule,
        catchup=False,
        tags=['Metereologia', 'Mapas']
    )
    def model_dag():

        cmd = f'/projetos/produtos-meteorologia/produtos.sh {model_name} "" "" "" "" ""'
        # cmd = f"ls /projetos/produtos-meteorologia/"

        BashOperator(
            task_id=f"run_{model_name}_script",
            bash_command=f"{SSH} '{cmd}'",
            execution_timeout=datetime.timedelta(hours=30),
        )

    return model_dag()

modelos_schedule = {
    'gfs': '0 2,8,14,20 * * *',
    'gefs': '0 3,8,15,20 * * *',
    'gefs-membros': '0 3,8,15,20 * * *',
    'gefs-estendido': '50 23 * * *',
    'gefs-estendido-membros': '2 0 * * *',
    'ecmwf': '0 4,17 * * *',
    'ecmwf-ens': '0 6,18 * * *',
    'ecmwf-ens-membros': '0 6,18 * * *',
    'ecmwf-aifs': '0 5,16 * * *',
    'ecmwf-aifs-ens': '0 5,16 * * *',
    'ecmwf-aifs-ens-membros': '0 5,16 * * *',
    'ecmwf-ens-estendido': '5 17 * * *',
    'ecmwf-ens-estendido-membros': '5 17 * * *'
}

for modelo, schedule in modelos_schedule.items():
    globals()[modelo.upper()] = create_model_dag(modelo, schedule)


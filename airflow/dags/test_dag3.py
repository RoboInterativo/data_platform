from airflow import DAG
from airflow.hooks.base_hook import BaseHook
from airflow.models import Variable
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.sql_sensor import SqlSensor
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator
#from airflow.contrib.hooks.mssql_hook import MsSqlHook
#from airflow.hooks.mssql_hook import MsSqlHook

import sqlalchemy as sa

def get_max_id():
    # Получаем последний ID из целевой таблицы
    max_id = BaseHook.get_connection("test").run(f"SELECT MAX(id) FROM target_table")[0]
    return max_id

def extract_transform_load( **kwargs):
    # Получаем параметры задачи
    ti = kwargs['ti']
    max_id = ti.xcom_pull(task_ids='get_max_id')
    # Создаем соединение с источником данных
    source_conn_id = "source_db"
    source_hook = MsSqlHook(mssql_conn_id=source_conn_id)
    # Выполняем запрос для получения новых записей
    new_records_query = f"SELECT  *  FROM source_table WHERE id > {max_id}"
    records = source_hook.get_records(new_records_query)
    # Вставляем новые записи в целевую таблицу
    target_conn_id = "target_db"
    target_hook = MsSqlHook(mssql_conn_id=target_conn_id)
    for record in records:
        target_hook.run(f"INSERT INTO target_table VALUES ({','.join(['?'] * len(record))})", record)

with DAG('SQLCOPY', start_date=days_ago(1), schedule_interval='@daily') as dag:
    # Задача для получения максимального ID из целевой таблицы
    get_max_id = PythonOperator(
        task_id='get_max_id',
        provide_context=True,
        python_callable=get_max_id
    )
    # Задача для проверки наличия новых записей перед их извлечением
    check_new_records = SqlSensor(
        task_id='check_new_records',
        poke_interval=5,
        sql="SELECT COUNT( * ) FROM source_table WHERE id > @max_id",
        params={'max_id': Variable.get('max_id', default_var=None)},
        hook=MsSqlHook(mssql_conn_id="test")
    )
    # Задача для извлечения, трансформации и загрузки данных
    etl = PythonOperator(
        task_id='etl',
        provide_context=True,
        python_callable=extract_transform_load
    )
    # Сетка задач
    get_max_id >> check_new_records >> etl

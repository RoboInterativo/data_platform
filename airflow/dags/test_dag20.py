from airflow import DAG
from airflow.hooks.base_hook import BaseHook
from airflow.models import Variable
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.sql_sensor import SqlSensor
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator
from airflow.providers.odbc.hooks.odbc import OdbcHook
import logging
from airflow.models import Variable


logger = logging.getLogger(__name__)
logger.info("This is a log message")

max_id = Variable.get("max_id", default_var=None)

#from airflow.contrib.hooks.mssql_hook import MsSqlHook
#from airflow.hooks.mssql_hook import MsSqlHook

import sqlalchemy as sa

# def get_max_id():
#     # Получаем последний ID из целевой таблицы
#     max_id = BaseHook.get_connection("my_prod_db").run(f"SELECT MAX(id) FROM dbo.events")[0]
#     logger.info("Max_id is",max_id)
#     return max_id

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

def print_context(ds=None, **kwargs):
    """Print the Airflow context and ds variable from the context."""
    print("::group::All kwargs")
    pprint(kwargs)
    print("::endgroup::")
    print("::group::Context variable ds")
    print(ds)
    print("::endgroup::")
    return "Whatever you return gets printed in the logs"

def use_hook( **kwargs):
    # Получаем параметры задачи
    # ti = kwargs['ti']
    # max_id = ti.xcom_pull(task_ids='get_max_id')
    # Создаем соединение с источником данных
    source_conn_id = "my_prod_db"
    source_hook =  OdbcHook( source_conn_id)
    print(source_hook)
    #MsSqlHook
    # Выполняем запрос для получhook_params={"schema":"estaff_cut"}ения новых записей
    new_records_query = f"SELECT COUNT (*)  FROM DimOrganization;"
    #records = source_hook.return_single_query_results(new_records_query,parameters=None)
    cnxn = source_hook.get_conn()
    cursor = cnxn.cursor()
    cursor.execute(new_records_query)
    row = cursor.fetchone()
    print (row)

def create_table( **kwargs):
    # Получаем параметры задачи
    # ti = kwargs['ti']
    # max_id = ti.xcom_pull(task_ids='get_max_id')
    # Создаем соединение с источником данных
    source_conn_id = "my_prod_db"
    source_hook =  OdbcHook( source_conn_id)

    dest_conn_id = "my_prod_db2"
    dest_hook =  OdbcHook( source_dest_id)
    # print(source_hook)
    # #MsSqlHook
    # # Выполняем запрос для получhook_params={"schema":"estaff_cut"}ения новых записей
    # new_records_query = f"SELECT COUNT (*)  FROM DimOrganization;"
    # #records = source_hook.return_single_query_results(new_records_query,parameters=None)
    # cnxn = source_hook.get_conn()
    # cursor = cnxn.cursor()
    # cursor.execute(new_records_query)
    # row = cursor.fetchone()
    # print (row)
    # get_records(new_records_query)
    # Вставляем новые записи в целевую таблицу
    # target_conn_id = "target_db"
    # target_hook = MsSqlHook(mssql_conn_id=target_conn_id)
    # for record in records:
    #     target_hook.run(f"INSERT INTO target_table VALUES ({','.join(['?'] * len(record))})", record)
    #return row

with DAG('SQLCOPY', start_date=days_ago(1), schedule_interval='@daily') as dag:

    # get_all_countries = MsSqlOperator(
    #         task_id="get_max_id",
    #         mssql_conn_id="my_prod_db",
    #         sql=r"""SELECT MAX(id) FROM dbo.events;""",
    #         hook_params={"schema":"estaff_cut"}
    # )
    #parameters={"id": max_id},
    get_max_id = PythonOperator(
            task_id="get_max_id", python_callable=use_hook
        )
    run_this = PythonOperator(
        task_id="print_the_context", python_callable=print_context
    )
    (
        get_max_id>>run_this
    )

    # Задача для получения максимального ID из целевой таблицы
    # get_countries_from_continent = MsSqlOperator(
    #     task_id="get_all_record",
    #     mssql_conn_id="my_prod_db",
    #     sql=r"""SELECT COUNT( * ) FROM dbo.events;""",
    #
    # )
    # get_max_id = PythonOperator(
    #     task_id='get_max_id',
    #     provide_context=True,
    #     python_callable=get_max_id
    # )
    # connection("my_prod_db").run(f"SELECT MAX(id) FROM dbo.events")[0]



    # Задача для проверки наличия новых записей перед их извлечением
    # check_new_records = SqlSensor(
    #     task_id='check_new_records',
    #     poke_interval=5,
    #     sql="SELECT COUNT( * ) FROM source_table WHERE id > @max_id",
    #     params={'max_id': Variable.get('max_id', default_var=None)},
    #     hook=MsSqlHook(mssql_conn_id="test")
    # )
    # # Задача для извлечения, трансформации и загрузки данных
    # etl = PythonOperator(
    #     task_id='etl',
    #     provide_context=True,
    #     python_callable=extract_transform_load
    # )
    # Сетка задач


    #>> check_new_records >> etl

from airflow import DAG
from airflow.hooks.base_hook import BaseHook
from airflow.models import Variable
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.sql_sensor import SqlSensor
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator
from airflow.operators.bash import BashOperator
import sqlalchemy.dialects as sqld
import gc

import os

from airflow.providers.odbc.hooks.odbc import OdbcHook
import logging
from airflow.models import Variable
from sqlalchemy import inspect, schema, Table
from airflow.providers.postgres.hooks.postgres import PostgresHook
from sqlalchemy.orm import Session
from sqlalchemy import insert
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
from sqlalchemy.types import (Integer, Float, Boolean, DateTime,
                                  Date, TIMESTAMP,BIGINT)



logger = logging.getLogger(__name__)
logger.info("This is a log message")

max_id = Variable.get("max_id", default_var=None)



import sqlalchemy as sa

# def push_function(**context):
#     msg='the_message'
#     print("message to push: '%s'" % msg)
#     task_instance = context['task_instance']
#     task_instance.xcom_push(key="the_message", value=msg)

def write_dashboard ( **kwargs):

    ti = kwargs['ti']
    print(ti)

    table_list = ti.xcom_pull(task_ids='get_tables', key='tables_list')
    print("TABLE LIST",table_list)
    #task_ids='push_task'

    dashboard_conn_id = "dashboard"
    dashboard_hook =  PostgresHook( dashboard_conn_id)

    db_engine =dashboard_hook.get_sqlalchemy_engine()
    session=Session(db_engine)

    table_name="dashboard_etl_table"

    db_metadata = schema.MetaData(bind=db_engine)
    db_table = Table(table_name, db_metadata, autoload=True)
    list1=[]
    for table in table_list:
        d={}
        d["table_name"]=table
        list1.append(d)


    session.execute(
         insert(db_table), list1
     )
    session.commit()

#
def load_table (**kwargs):
    def __get_pyarrowtype(column, sqltype):
            # logger = logging.getLogger(__name__)
            # logger.info(f"{column.name} Start process ")


            if isinstance(sqltype, Float):
                return pa.float64()
            elif isinstance(sqltype, BIGINT):
                # if column.nullable:
                #     return np.dtype( 'double')
                # else:
                return pa.int64()
                # if (column.name in ['group_event_id', 'group_id', 'vacancy_id']):
                #     return  np.str_
                # else.

            elif isinstance(sqltype, Integer):
               # if (column.name in ['group_event_id', 'group_id', 'vacancy_id']):
               #     return  np.str_
               # else:
                return pa.int64()
            elif isinstance(sqltype, TIMESTAMP):
                # we have a timezone capable type
                # if not sqltype.timezone:
                #     return np.dtype('datetime64[ns]')
                return pa.pa.timestamp('us')
            elif isinstance(sqltype, DateTime):
                return pa.timestamp('us')
        #         return np.dtype('datetime64[ns]')
        #             elif isinstance(sqltype, DateTime):
        # # Caution: np.datetime64 is also a subclass of np.number.

            elif isinstance(sqltype, Date):
                return pa.date32()
            elif isinstance(sqltype, Boolean):
                return pa.bool_()
            elif isinstance(sqltype, sqld.mssql.base.BIT):
                # Handling database provider specific types
                return pa.uint8()
            # Catch all type - handle provider specific types in another elif block
            return pa.string()
    #START MAIN
    skip_tables=["(spxml_large_fields)","(spxml_static_urls)", "vacancy_request_templates_1000" ]

    source_conn_id = "my_prod_db"
    source_hook =  OdbcHook( source_conn_id)
    print(source_hook)
    db_engine =source_hook.get_sqlalchemy_engine()
    inspector = inspect(db_engine)
    # schemas = inspector.get_schema_names()
    table_schema='dbo'
    #--------------
    ti = kwargs['ti']
    print(ti)

    table_list = ti.xcom_pull(task_ids='get_tables', key='tables_list')

    print("TABLES",table_list)

    #---------------
    tables_size_list = kwargs['ti'].xcom_pull(task_ids='get_record_size', key='tables_size')
    if tables_size_list is None:
        kwargs['ti'].xcom_push(key='tables_size', value={})
        tables_size_list={}
    print("!!!TABLE SIZE LIST",tables_size_list)
    skip_tables.extend(list(tables_size_list.keys()))
    print ( " This tables skipted",skip_tables)
    for table_name in table_list:
        if (not ( table_name in skip_tables)):
        # for table_name in inspector.get_table_names(schema=table_schema):
            #table_name="events"
            db_metadata = schema.MetaData(bind=db_engine)

            logger.info(f"process {table_name} TABLE....")
            db_table = Table(table_name, db_metadata, autoload=True)
        #Start
            s_shema=[]
            d_shema=[]
            col=[]
            col2=[]
            for column in db_table.columns:
                dtype=__get_pyarrowtype(column,column.type)
                print (column.name,dtype,(column.type))


                #print(dtype)
                if  isinstance(column.type, DateTime):
                    item2=pa.field(column.name, pa.string ())
                    col2.append(column.name)
                else:
                    item2=pa.field(column.name, dtype )
                    col2.append(column.name)


                item=pa.field(column.name, dtype )
                s_shema.append(item)
                d_shema.append(item2)

            pa_shema=pa.schema(s_shema)
            pa_dshema=pa.schema(d_shema)
            result = db_table.select().execute()

            # row_batch = result.fetchmany(size=100)
            # import os
            batch_size=1000
            logger.info(f"fetch START {table_name}_{batch_size}.records ....")
            row_batch = result.fetchmany(size=batch_size)
            logger.info(f"fetch END {table_name}_{batch_size}.records ....")
            # append = False
            i=1


            while(len(row_batch) > 0):

                print(i)
                logger.info(f"process START {table_name}_{i}.parquet FILE....")

        # pa_shema
                table=pa.Table.from_pylist(row_batch,schema=pa_shema)
                arr=[]
                for col in table.columns:
                    if col.type ==pa.timestamp('us'):
                        arr.append(col.cast(pa.string() ))
                    else:
                        arr.append(col)
                dest_data = pa.Table.from_arrays(arr, schema=pa_dshema)

                #logger.info("USAGE " + str(b_df.memory_usage) )
                logger.info(f"process END {table_name}_{i}.parquet FILE....")
                # write data
                #table = pa.Table.from_pandas(b_df, preserve_index=False)
                # table=pa.Table.from_pylist(row_batch)

                pq.write_table(dest_data, f'/opt/airflow/logs/test_{table_name}_{i}.parquet',
                    use_deprecated_int96_timestamps=True

                )
                # b_df.to_parquet(f'/opt/airflow/logs/{table_name}_{i}.parquet', engine='pyarrow' ,use_deprecated_int96_timestamps=True)
                del table
                del dest_data
                del arr
                gc.collect()
                 #№,coerce_timestamps="ms")
                #i+=1
                # append = True
                logger.info(f"fetch START {table_name}_{batch_size}.records ....")
                row_batch = []#result.fetchmany(size=batch_size)
                logger.info(f"fetch END {table_name}_{batch_size}.records ....")
                # Вычисление размера Parquet файла
                file_path = Path(  f'/opt/airflow/logs/test_{table_name}_{i}.parquet')
                parquet_size = file_path.stat().st_size
                #os.remove()
                print(f"Размер Parquet файла: {parquet_size} байт")
                print(f"Размер 1 записи: {parquet_size/1000} байт")
                tables_size_list[table_name]=parquet_size/1000
                #table_size = kwargs['ti'].xcom_pull(task_ids='get_record_size', key='tables_size')
                kwargs['ti'].xcom_push(key='tables_size', value=tables_size_list)

#end


def get_record_size (**kwargs):
    source_conn_id = "my_prod_db"
    source_hook =  OdbcHook( source_conn_id)
    print(source_hook)
    db_engine =source_hook.get_sqlalchemy_engine()
    inspector = inspect(db_engine)
    # schemas = inspector.get_schema_names()
    table_schema='dbo'

    # for table_name in inspector.get_table_names(schema=table_schema):
    table_name="events"
    db_metadata = schema.MetaData(bind=db_engine)

    logger.info(f"process {table_name} TABLE....")
    db_table = Table(table_name, db_metadata, autoload=True)
#Start


    result = db_table.select().execute()

    # row_batch = result.fetchmany(size=100)
    # import os
    batch_size=1000
    logger.info(f"fetch START {table_name}_{batch_size}.records ....")
    row_batch = result.fetchmany(size=batch_size)
    df=pd.DataFrame.from_records(row_batch)
    logger.info(f"fetch END {table_name}_{batch_size}.records ....")
    # append = False

    record_sizes = df.memory_usage(deep=True).values

    # Вычисление среднего размера записи
    average_size = record_sizes.mean()
    print(average_size)





def get_tables (**kwargs):
#




    source_conn_id = "my_prod_db"
    source_hook =  OdbcHook( source_conn_id)
    print(source_hook)
    db_engine =source_hook.get_sqlalchemy_engine()
    inspector = inspect(db_engine)
    table_schema='dbo'

    for table_name in inspector.get_table_names(schema=table_schema):
        print(table_name)


    table_list=list(inspector.get_table_names(schema=table_schema))
    """Pushes an XCom without a specific target"""
    kwargs['ti'].xcom_push(key='tables_list', value=table_list)
    #ti.xcom_push(key="tables_list", task_ids="gettables",value=table_list )
    # new_records_query = f"SELECT COUNT (*)  FROM dbo.events;"
    #
    # cnxn = source_hook.get_conn()_
    # cursor = cnxn.cursor()
    # cursor.execute(new_records_query)
    # row = cursor.fetchone()
    # print (row)


with DAG('TEST_SIZE', start_date=days_ago(1), schedule_interval='@daily') as dag:

    # get_all_countries = MsSqlOperator(
    #         task_id="get_max_id",
    #         mssql_conn_id="my_prod_db",
    #         sql=r"""SELECT MAX(id) FROM dbo.events;""",
    #         hook_params={"schema":"estaff_cut"}
    # )
    #parameters={"id": max_id},
    # gettables = PythonOperator(
    #         task_id="gettables", python_callable=get_tables,provide_context=True
    #     )
    step1 = BashOperator(
            task_id="step1",
            bash_command='echo eXB4021205Bia$ |kinit ashilo ',
    )
    get_tables=PythonOperator(
            task_id="get_tables", python_callable=get_tables, provide_context=True
    )
    # !
    get_record_size=PythonOperator(
                    task_id="get_record_size", python_callable=load_table, provide_context=True
    )





    (
        step1>>get_tables>>get_record_size
        #>>gettables>>write2dashboard
    )

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.decorators import task, dag
from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator
import time
from datetime import datetime, timedelta
import pyodbc
import logging
import gc

import os
import pandas as pd
import numpy as np
import fastparquet
import pyodbc
import sqlalchemy as sa
from sqlalchemy import create_engine, schema, Table
from sqlalchemy import inspect
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq



from subprocess import Popen, PIPE
import pandas as pd
import os, json, boto3, pathlib,  requests
from hdfs import Client
import sqlalchemy.dialects as sqld
from sqlalchemy.types import (Integer, Float, Boolean, DateTime,
                                  Date, TIMESTAMP,BIGINT)


default_args = {
    "start_date": datetime(2022, 1, 1)
}



@dag(
    schedule_interval=None,
    default_args=default_args,
    catchup=False, dagrun_timeout=timedelta(minutes=50), concurrency=2, max_active_runs=1)
def my_dag2():

    @task(task_id='testsql_hdfs')
    def test_sql():
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
                return pa.timestamp('us')
            elif isinstance(sqltype, Boolean):
                return pa.bool_()
            elif isinstance(sqltype, sqld.mssql.base.BIT):
                # Handling database provider specific types
                return pa.uint8()
            # Catch all type - handle provider specific types in another elif block
            return pa.string()
    

        
        
        # for schema in schemas:
        #     print("schema: %s" % schema)
        # schema='dbo'
        logger = logging.getLogger(__name__)
        logger.info("Start process")
        # for table_name in inspector.get_table_names(schema=schema):
        #         print (table_name)
        #         logger.info(f"process {table_name} TABLE....")
        # #         # for column in inspector.get_columns(table_name, schema=schema):
        # #         #     print("Column: %s" % column)
        # len(inspector.get_table_names(schema=schema))
        
        
        
        DEFAULT_DRIVER = "pyodbc"
        DEFAULT_ODBC_DRIVER = "ODBC Driver 17 for SQL Server"
        database={
        "name": "estaff_cut",
        "mssql.driver": "pyodbc",
        "pyodbc.config": "ODBC Driver 17 for SQL Server",
        "hostname": "t-estaff-dl.dellin.local",
        "port": "1433",
        "user": "dellin\\ashilo",
        "password": "eXB4021205Bia$"}
        
        password="eXB4021205Bia$"
        userid='ashilo'
        # kinit = '/usr/bin/kinit'
        # kinit_args = [ kinit, userid ]
        # kinit = Popen(kinit_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        # kinit.stdin.write( bytes('{}/n'.format(password) ,"UTF8"))
        #
        # kinit.wait()
        
        driver_config = database.get("pyodbc.config")
        import urllib
        
        params = urllib.parse.quote_plus(f"DRIVER={DEFAULT_ODBC_DRIVER};"
                                         f"SERVER={database['hostname']};"
                                         f"DATABASE={database['name']};"
                                         f"Trusted_Connection=yes")
        db_engine = sa.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
        # db_engine =engine# create_engine(con)
        db_metadata = schema.MetaData(bind=db_engine)
        
        inspector = inspect(db_engine)
        # schemas = inspector.get_schema_names()
        table_schema='dbo'
        
        # for table_name in inspector.get_table_names(schema=table_schema):
        table_name="events"
#inspector.get_table_names(schema=table_schema)[0]
        #for
        logger.info(f"process {table_name} TABLE....")
        db_table = Table(table_name, db_metadata, autoload=True)
        shema=[]
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
            shema.append(item)
            d_shema.append(item2)        

        pa_shema=pa.schema(shema)
        pa_dshema=pa.schema(d_shema)
        result = db_table.select().execute()
        
        # row_batch = result.fetchmany(size=100)
        # import os
        batch_size=900000
        logger.info(f"fetch START {table_name}_{batch_size}.records ....")
        row_batch = result.fetchmany(size=batch_size)
        logger.info(f"fetch END {table_name}_{batch_size}.records ....")
        # append = False
        i=1

        import sqlalchemy

        #fields=column_dict2.keys()
        #['id','group_event_id','group_id']
        # print(b_df[fields])
        #def field_by_name(field): return list(column_dict.keys()).index(field)
        #fields=['id','group_event_id','group_id']
        
    
        
        #print (row[field_by_name(f)],' ',end='')
# print(l)
        
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
            
            pq.write_table(dest_data, f'/opt/airflow/logs/{table_name}_{i}.parquet',
                use_deprecated_int96_timestamps=True
              
            )
            # b_df.to_parquet(f'/opt/airflow/logs/{table_name}_{i}.parquet', engine='pyarrow' ,use_deprecated_int96_timestamps=True)
            del table
            del dest_data
            del arr
            gc.collect()
             #№,coerce_timestamps="ms")
            i+=1
            # append = True 
            logger.info(f"fetch START {table_name}_{batch_size}.records ....")
            row_batch = result.fetchmany(size=batch_size)
            logger.info(f"fetch END {table_name}_{batch_size}.records ....")



 
            #         __write_parquet(output_path, row_batch,
            #                         column_dict, write_index, compression, append)

          
           


    test_sql()


sqltestdag = my_dag2()

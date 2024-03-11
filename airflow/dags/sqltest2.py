from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.decorators import task, dag
from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator
import time
from datetime import datetime, timedelta
import pyodbc
import os
from subprocess import Popen, PIPE
import pandas as pd
import os, json, boto3, pathlib,  requests
from hdfs import Client


default_args = {
    "start_date": datetime(2022, 1, 1)
}



@dag(
    schedule_interval=None,
    default_args=default_args,
    catchup=False, dagrun_timeout=timedelta(minutes=10), concurrency=2, max_active_runs=1)
def my_dag2():

    @task(task_id='testsql_hdfs')
    def test_sql():
        # server="Server"
        # username="User"
        # password="Password"
        # database="master"
        # ddw_connection = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password+';TrustServerCertificate=yes;')
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
        kinit = '/usr/bin/kinit'
        kinit_args = [ kinit, userid ]
        kinit = Popen(kinit_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        kinit.stdin.write( bytes('{}/n'.format(password) ,"UTF8"))
        #
        # kinit.wait()

        driver_config = database.get("pyodbc.config")
        connection_lnk_pyodbc = f"DRIVER={driver_config};" \
                                                       f"SERVER={database['hostname']};" \
                                                       f"DATABASE={database['name']};" \
                                                       f"APP=CDC Connector;" \
                                                       f"Encrypt=yes;" \
                                                       f"TrustServerCertificate=yes;" \
                                                       f"Authentication=ActiveDirectoryIntegrated;" \
                                                       f"UID={database['user']}"


        ddw_connection = pyodbc.connect(connection_lnk_pyodbc, autocommit=True)

        query1 ="""SELECT
          *
        FROM
          SYSOBJECTS
        WHERE
          xtype = 'U';
        """
        query1="""SELECT
           * FROM events

        """
        print(query1)
        print(ddw_connection)
        i=0
#         s3_target = boto3.resource('s3',
#     endpoint_url='https://<minio>:9000',
#     aws_access_key_id='<key_id>',
#     aws_secret_access_key='<access_key>',
#     aws_session_token=None,
#     config=boto3.session.Config(signature_version='s3v4'),
#     verify=False
# output = subprocess.Popen(['k', '-l', Path.home()], text=True,
#     stdout=subprocess.PIPE)

        aws_access_key_id = "wvz6mEC2lZqoSzqprmjG"
        aws_secret_access_key = "eoDasbrwXlnKOAxI7kRgEJ3QhlbQdSgJ3bIXRzd7"
        conf_s3={"aws_secret_access_key": aws_secret_access_key,
            "aws_access_key_id":aws_access_key_id,
            "service_name":"s3",
            "bucket_name":"test"    }

        for chunk_dataframe in pd.read_sql(
            query1, ddw_connection, chunksize=500000):
            print(f"Got dataframe w/{len(chunk_dataframe)} rows")
            i=i+1

            chunk_dataframe.to_parquet('/tmp/myfile_{}.parquet'.format(str (i)), engine='pyarrow')
            client=Client('http://10.214.3.111:9870')
            # s3_client = boto3.client(
            #     endpoint_url='http://10.182.36.23:9000',
            #     service_name=conf_s3["service_name"],
            #     aws_access_key_id=conf_s3["aws_access_key_id"],
            #     aws_secret_access_key=conf_s3["aws_secret_access_key"])
            #
            # with client.write('/user/root/helloworld.csv', encoding = 'utf-8') as writer:
            #     df.to_csv(writer)
            # s3_client.upload_file(
            #     "/tmp/myfile_{}.parquet".format(str (i)),
            #     conf_s3["bucket_name"],
            #     "myfile_{}.parquet".format(str (i))
            #     )
            fname='myfile_{}.parquet'.format(str (i))
            client.upload(f"/user/root/test/{fname}", f"/tmp/{fname}" )

            os.remove(f"/tmp/{fname}" )


            # if i>10:
            #     break
        # cursor = ddw_connection.cursor()
        # queryresult  = cursor.execute(query1)
        #
        #
        # records = cursor.fetchone()
        # print (records)
   ##database_names    = [db.ddw_databasename for db in databases_to_sync]


    test_sql()


sqltestdag = my_dag2()

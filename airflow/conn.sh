airflow connections add 'my_prod_db'     \
--conn-json '{"conn_type": "odbc", "host": "sqlserver", "port": 1433, "extra": {"DRIVER": "ODBC Driver 17 for SQL Server", "SERVER": "t-estaff-dl.dellin.local", "DATABASE": "estaff_cut", "Trusted_Connection": "yes"}}'

airflow connections add 'my_prod_db'     \
--conn-json '{"conn_type": "odbc", "host": "sqlserver", "port": 1433, "extra": {"DRIVER": "ODBC Driver 17 for SQL Server", "SERVER": "t-estaff-dl.dellin.local", "DATABASE": "test", "Trusted_Connection": "yes"}}'

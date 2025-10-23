airflow connections add 'my_prod_db'     \
--conn-json '{"conn_type": "odbc", "host": "sqlserver", "port": 1433, "login": "SA",password": "exb021025!","schema": "AdventureWorksDW2022","extra": {"DRIVER": "ODBC Driver 17 for SQL Server", "SERVER": "sqlserver", "DATABASE": "AdventureWorksDW2022"}}'

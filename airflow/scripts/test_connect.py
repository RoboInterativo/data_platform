#config_connector = Conf(config_file)
import pyodbc
DEFAULT_DRIVER = "pyodbc"
DEFAULT_ODBC_DRIVER = "ODBC Driver 17 for SQL Server"
database={
"name": "test",
"mssql.driver": "pyodbc",
"pyodbc.config": "ODBC Driver 17 for SQL Server",
"hostname": "sqlserver",
"port": "1433",
"user": "test",
"password": "Password!"}


driver_config = database.get("pyodbc.config")
#UID={USERNAME};PWD={PASSWORD}'
connection_lnk_pyodbc = f"DRIVER={driver_config};" \
                                               f"SERVER={database['hostname']};" \
                                               f"DATABASE={database['name']};" \
                                               "INTEGRATED SECURITY=SSPI;" \
                                               f"PWD={database['password']};" \
                                               "UID=SA"
# connection_lnk_pyodbc = f"DRIVER={driver_config};" \  "TRUSTED_CONNECTION=YES;" \
#                                                f"SERVER={database['hostname']};" \
#                                                f"DATABASE={database['name']};" \
#                                                f"APP=CDC Connector;" \
#                                                f"Encrypt=yes;" \
#                                                f"TrustServerCertificate=yes;" \
#                                                f"Authentication=ActiveDirectoryIntegrated;" \
#                                                f"UID={database['user']}"
#

engine = pyodbc.connect(connection_lnk_pyodbc, autocommit=True)

SQL_QUERY="""SELECT
  *
FROM
  SYSOBJECTS
WHERE
  xtype = 'U';
"""


cursor = engine.cursor()
cursor.execute(SQL_QUERY)
records = cursor.fetchall()
print (records)

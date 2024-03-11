#config_connector = Conf(config_file)
import pyodbc
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


driver_config = database.get("pyodbc.config")
connection_lnk_pyodbc = f"DRIVER={driver_config};" \
                                               f"SERVER={database['hostname']};" \
                                               f"DATABASE={database['name']};" \
                                               f"APP=CDC Connector;" \
                                               f"Encrypt=yes;" \
                                               f"TrustServerCertificate=yes;" \
                                               f"Authentication=ActiveDirectoryIntegrated;" \
                                               f"UID={database['user']}"


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

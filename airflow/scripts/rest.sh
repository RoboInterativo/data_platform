export PATH=$PATH:/opt/mssql-tools/bin
sqlcmd -S localhost -U SA -P Password! \
-Q """RESTORE DATABASE dbname
FROM DISK = '/data/AdventureWorksDW2022.bak'
WITH MOVE 'Dbname_Empty' TO '/data/dbname.mdf',
MOVE 'Dbname_Empty_log' TO '//data/dbname.ldf'
"""
#'/data/AdventureWorksDW2022.bak' WITH FILE = 1, NOUNLOAD, REPLACE, NORECOVERY, STATS = 5"

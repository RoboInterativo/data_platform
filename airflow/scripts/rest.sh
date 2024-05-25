export PATH=$PATH:/opt/mssql-tools/bin
sqlcmd -S localhost -U SA -P Password! \
-Q """RESTORE DATABASE AdventureWorksDW2022
FROM DISK = '/data/AdventureWorksDW2022.bak'
WITH MOVE 'AdventureWorksDW2022' TO '/data/AdventureWorksDW2022.mdf',
MOVE 'AdventureWorksDW2022_log' TO '/data/AdventureWorksDW2022.ldf'
"""
#'/data/AdventureWorksDW2022.bak' WITH FILE = 1, NOUNLOAD, REPLACE, NORECOVERY, STATS = 5"

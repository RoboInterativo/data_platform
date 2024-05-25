export PATH=$PATH:/opt/mssql-tools/bin
sqlcmd -S localhost -U SA -P Password! \
-Q "RESTORE DATABASE [demodb] FROM DISK = '/data/AdventureWorksDW2022.bak' WITH FILE = 1, NOUNLOAD, REPLACE, NORECOVERY, STATS = 5"

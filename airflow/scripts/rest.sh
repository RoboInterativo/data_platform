sqlcmd -S localhost -U SA -P Password! \
-Q "RESTORE DATABASE [demodb] FROM DISK = N'/data/AdventureWorksDW2022.bak' WITH FILE = 1, NOUNLOAD, REPLACE, NORECOVERY, STATS = 5"

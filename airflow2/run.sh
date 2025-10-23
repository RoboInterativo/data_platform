HOSTS="t-estaff-dl.dellin.local:10.214.72.23"

docker run --add-host  $HOSTS -it airflow-s3-mssql  bash

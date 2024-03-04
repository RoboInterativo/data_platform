curl -i -X POST -H "Accept:application/json" \
  -H  "Content-Type:application/json" \
  http://172.17.0.1:8083/connectors/ \
  -d @pg.json

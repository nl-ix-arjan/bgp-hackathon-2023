# bgp-hackathon-2023

How to get clickhouse running with the compose file in this repo:

```
docker-compose up
```

How to get a client console up:

```
docker-compose exec clickhouse clickhouse-client --output_format_pretty_color true
```

How I inserted the CSVs:

```
docker-compose exec -T clickhouse clickhouse-client -q "INSERT INTO bgp_updates_ipv4 FORMAT CSV" < updates.20230602.0025.csv
docker-compose exec -T clickhouse clickhouse-client -q "INSERT INTO bgp_updates_ipv4 FORMAT CSV" < updates.20230602.0030.csv
docker-compose exec -T clickhouse clickhouse-client -q "INSERT INTO bgp_updates_ipv4 FORMAT CSV" < updates.20230602.0030.csv
docker-compose exec -T clickhouse clickhouse-client -q "INSERT INTO bgp_updates_ipv4 FORMAT CSV" < updates.20230602.0035.csv
docker-compose exec -T clickhouse clickhouse-client -q "INSERT INTO bgp_updates_ipv4 FORMAT CSV" < updates.20230602.0040.csv
```

# bgp-hackathon-2023

How to get clickhouse running with the compose file in this repo:

```
docker-compose up
```

How to get a client console up:

```
docker-compose exec clickhouse clickhouse-client --output_format_pretty_color true
```

The data schema:

```
CREATE TABLE IF NOT EXISTS bgp_updates_ipv4 (
  timestamp DateTime,
  router_ip IPv4,
  message_type Enum('withdrawal'=0, 'announcement'=1),
  peer_ip IPv4,
  peer_asn UInt32,
  prefix_ip IPv4,
  prefix_length UInt8,
  next_hop_ip IPv4 DEFAULT '0.0.0.0',
  as_path Array(UInt32),
  small_communities Array(String),
  large_communities Array(String)
)
ENGINE = MergeTree()
PARTITION BY (router_ip, toYYYYMMDD(timestamp))
PRIMARY KEY (message_type, router_ip, prefix_length, prefix_ip)
ORDER BY (message_type, router_ip, prefix_length, prefix_ip, timestamp, next_hop_ip)
```

How I inserted the CSVs:

```
docker-compose exec -T clickhouse clickhouse-client -q "INSERT INTO bgp_updates_ipv4 FORMAT CSV" < updates.20230602.0025.csv
docker-compose exec -T clickhouse clickhouse-client -q "INSERT INTO bgp_updates_ipv4 FORMAT CSV" < updates.20230602.0030.csv
docker-compose exec -T clickhouse clickhouse-client -q "INSERT INTO bgp_updates_ipv4 FORMAT CSV" < updates.20230602.0030.csv
docker-compose exec -T clickhouse clickhouse-client -q "INSERT INTO bgp_updates_ipv4 FORMAT CSV" < updates.20230602.0035.csv
docker-compose exec -T clickhouse clickhouse-client -q "INSERT INTO bgp_updates_ipv4 FORMAT CSV" < updates.20230602.0040.csv
```

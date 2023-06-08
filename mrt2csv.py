#!/usr/bin/env python3

import csv
import ipaddress
import sys
from pprint import pprint

from mrtparse import Reader


def main():
    csv_writer = csv.writer(sys.stdout, dialect="unix")

    for entry in Reader(sys.argv[1]):
        try:
            for row in make_csv_rows_from_entry(entry.data):
                csv_writer.writerow(row)

        except Exception as e:
            print(f"error while parsing data: {repr(e)}")
            pprint(entry.data)
            raise


def make_csv_rows_from_entry(entry: dict):
    subtype = get_enum_name(entry["subtype"])

    if subtype != "BGP4MP_MESSAGE_AS4":
        # we only want BGP-4 messages
        return

    bgp_message = entry["bgp_message"]
    bgp_message_type = get_enum_name(bgp_message["type"])

    if bgp_message_type != "UPDATE":
        # we skip everything but UDATE messages
        return

    timestamp = get_timestamp_int(entry["timestamp"])
    router_ip = entry["local_ip"]
    peer_ip = entry["peer_ip"]
    peer_asn = entry["peer_as"]

    # skip ipv6 for now

    if not is_ipv4_address(peer_ip):
        return

    # withdrawals

    withdrawn_routes = bgp_message["withdrawn_routes"]

    for withdrawal in withdrawn_routes:
        prefix_ip = withdrawal["prefix"]
        prefix_length = withdrawal["length"]
        yield (
            timestamp,
            router_ip,
            "withdrawal",
            peer_ip,
            peer_asn,
            prefix_ip,
            prefix_length,
            "0.0.0.0",  # representing next-hop as this to prevent null/empty outputs; agh
            [],  # no as-path
            [],  # no small communities
            [],  # no large communities
        )

    # announcements

    path_attributes = bgp_message["path_attributes"]

    if path_attributes:
        as_path = get_component_value(path_attributes, "AS_PATH")
        as_sequence = get_component_value(as_path, "AS_SEQUENCE") if as_path else None
        as_path_values = list(map(int, as_sequence)) if as_sequence else None
        next_hop = get_component_value(path_attributes, "NEXT_HOP")
        small_communities = get_component_value(path_attributes, "COMMUNITY")
        large_communities = get_component_value(path_attributes, "LARGE_COMMUNITY")

        for nlri in bgp_message["nlri"]:
            prefix_ip = nlri["prefix"]
            prefix_length = nlri["length"]
            yield (
                timestamp,
                router_ip,
                "announcement",
                peer_ip,
                peer_asn,
                prefix_ip,
                prefix_length,
                next_hop,
                as_path_values,
                small_communities,
                large_communities,
            )


def is_ipv4_address(value: str) -> bool:
    return isinstance(ipaddress.ip_address(value), ipaddress.IPv4Address)


def get_enum_name(enum: dict) -> str:
    return next(iter(enum.values()))


def get_timestamp_int(value: dict) -> int:
    return next(iter(value.keys()))


def get_component_value(attributes: list[dict], type: str):
    for attribute in attributes:
        if get_enum_name(attribute["type"]) == type:
            return attribute["value"]

    else:
        return None


main()

#
# this is an example of an entry.data item
#
example_data = (
    {
        "timestamp": {"1686075599": "2023-06-06 20:19:59"},
        "type": {"16": "BGP4MP"},
        "subtype": {"4": "BGP4MP_MESSAGE_AS4"},
        "length": 128,
        "peer_as": "57406",
        "local_as": "12654",
        "ifindex": 0,
        "afi": {"1": "IPv4"},
        "peer_ip": "193.239.116.239",
        "local_ip": "193.239.116.45",
        "bgp_message": {
            "marker": "ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff",
            "length": 108,
            "type": {"2": "UPDATE"},
            "withdrawn_routes_length": 0,
            "withdrawn_routes": [],
            "path_attributes_length": 81,
            "path_attributes": [
                {
                    "flag": 64,
                    "type": {"1": "ORIGIN"},
                    "length": 1,
                    "value": {"0": "IGP"},
                },
                {
                    "flag": 64,
                    "type": {"2": "AS_PATH"},
                    "length": 14,
                    "value": [
                        {
                            "type": {"2": "AS_SEQUENCE"},
                            "length": 3,
                            "value": ["57406", "9318", "18033"],
                        }
                    ],
                },
                {
                    "flag": 64,
                    "type": {"3": "NEXT_HOP"},
                    "length": 4,
                    "value": "193.239.116.239",
                },
                {
                    "flag": 128,
                    "type": {"4": "MULTI_EXIT_DISC"},
                    "length": 4,
                    "value": 0,
                },
                {
                    "flag": 192,
                    "type": {"8": "COMMUNITY"},
                    "length": 16,
                    "value": ["65101:1085", "65102:1000", "65103:276", "65104:150"],
                },
                {
                    "flag": 224,
                    "type": {"32": "LARGE_COMMUNITY"},
                    "length": 24,
                    "value": ["6695:1000:2", "6695:1001:1"],
                },
            ],
            "nlri": [{"length": 24, "prefix": "49.143.186.0"}],
        },
    },
)

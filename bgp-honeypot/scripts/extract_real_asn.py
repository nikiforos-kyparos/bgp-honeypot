#!/usr/bin/env python3

import ipaddress
import json
import os
import sys
import time
import urllib.request
import urllib.error

BATCH_SIZE = 500
API_URL = "https://api.ipinfo.io/batch"


def read_ips(path):
    ips = set()
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            ip = line.strip().split("\t")[0]
            if not ip:
                continue
            try:
                ipaddress.IPv4Address(ip)
                ips.add(ip)
            except ValueError:
                pass
    return sorted(ips)


def chunks(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def ipinfo_batch_lookup(ips, token):
    paths = [f"/lite/{ip}" for ip in ips]

    req = urllib.request.Request(
        f"{API_URL}?token={token}",
        data=json.dumps(paths).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def extract_asn(value):
    if not isinstance(value, dict):
        return None

    asn = value.get("asn")
    if not asn:
        return None

    asn = str(asn).strip().upper()
    if asn.startswith("AS"):
        asn = asn[2:]

    return int(asn) if asn.isdigit() else None


def main():

    token = os.environ.get("IPINFO_TOKEN")

    ips = read_ips(sys.argv[1])

    asns = set()

    for batch_num, batch in enumerate(chunks(ips, BATCH_SIZE), start=1):
        result = ipinfo_batch_lookup(batch, token)

        for ip in batch:
            value = result.get(f"lite/{ip}") or result.get(f"/lite/{ip}") or result.get(ip)
            asn = extract_asn(value)
            if asn is not None:
                asns.add(asn)

        print(f"Processed batch {batch_num}", file=sys.stderr)
        time.sleep(0.2)

    for asn in sorted(asns):
        print(asn)

    print(f"\nUnique real ASN count: {len(asns)}", file=sys.stderr)
    print(f"Unique IPv4s checked: {len(ips)}", file=sys.stderr)

if __name__ == "__main__":
    main()

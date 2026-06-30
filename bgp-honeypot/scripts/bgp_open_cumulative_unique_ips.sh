#!/bin/bash

PCAP_DIR="/path/to/pcaps"
OUTPUT="bgp_open_cumulative_unique_ips.csv"
SEEN_IPS_FILE="seen_bgp_open_ips.txt"

echo "date,daily_total_open_packets,daily_unique_ips,cumulative_unique_ips" > "$OUTPUT"

> "$SEEN_IPS_FILE"

for pcap in $(ls "$PCAP_DIR"/*.pcap 2>/dev/null | sort); do

day=$(tshark -r "$pcap" -T fields -e frame.time_epoch -c 1 2>/dev/null \
    | awk '{ print strftime("%d/%m", $1) }')

tmp_ips=$(mktemp)

tshark -r "$pcap" \
    -Y "bgp.type == 1 && !(ip.src == honeypot.initial.ip.here) && !(ip.src == honeypot.range.here)" \
    -T fields \
    -e ip.src 2>/dev/null \
    | sed '/^$/d' > "$tmp_ips"

daily_total=$(wc -l < "$tmp_ips")
daily_unique=$(sort -u "$tmp_ips" | wc -l)

cat "$tmp_ips" >> "$SEEN_IPS_FILE"
cumulative_unique=$(sort -u "$SEEN_IPS_FILE" | wc -l)

echo "$day,$daily_total,$daily_unique,$cumulative_unique" >> "$OUTPUT"

rm "$tmp_ips"

done

sort -u "$SEEN_IPS_FILE" -o "$SEEN_IPS_FILE"

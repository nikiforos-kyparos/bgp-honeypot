#!/bin/bash

PCAP_DIR="path/to/pcaps"
OUTPUT="bgp_open_ip_reported_asn_by_day.csv"

HONEYPOT_IP="honeypot_ip"
HONEYPOT_RANGE="honeypot_range"

asn_field="bgp.open.myas"

echo "date,src_ip,reported_asn" > "$OUTPUT"

for pcap in $(find "$PCAP_DIR" -type f -name "*.pcap" | sort); do

day=$(tshark -r "$pcap" -T fields -e frame.time_epoch -c 1 2>/dev/null \
    | awk '{ print strftime("%d/%m", $1) }')

count_before=$(wc -l < "$OUTPUT")

tshark -r "$pcap" \
    -Y "bgp.type == 1 && !(ip.src == $HONEYPOT_IP) && !(ip.src == $HONEYPOT_RANGE)" \
    -T fields \
    -E separator=, \
    -E occurrence=f \
    -e ip.src \
    -e "$asn_field" \
    2>/dev/null | awk -F',' -v day="$day" '
        {
            ip=$1
            reported_asn=$2

            if (ip != "") {
                if (reported_asn == "") {
                    reported_asn="UNKNOWN"
                }

                print day "," ip "," reported_asn
            }
        }
    ' >> "$OUTPUT"

count_after=$(wc -l < "$OUTPUT")
added=$((count_after - count_before))

done

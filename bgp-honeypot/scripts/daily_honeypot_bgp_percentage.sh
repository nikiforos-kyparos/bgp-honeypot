OUT="daily_honeypot_bgp_percentage.csv"

echo "date,total_packets,bgp_packets,bgp_percentage" > "$OUT"

for f in /path/to/pcaps/*.pcap*; do
    base=$(basename "$f")

    raw_day=$(echo "$base" | grep -oE '[0-9]{8}' | head -n 1 || true)
        if [ -n "$raw_day" ]; then
            day="${raw_day:0:4}-${raw_day:4:2}-${raw_day:6:2}"
       fi

    total_packets=$(tshark -r "$f" -T fields -e frame.number 2>/dev/null | tail -n 1)

    bgp_packets=$(tshark -r "$f" \
        -Y "bgp" \
        -T fields -e frame.number 2>/dev/null | wc -l | tr -d ' ')

    if [ -n "$total_packets" ] && [ "$total_packets" -gt 0 ]; then
        pct=$(awk -v b="$bgp_packets" -v t="$total_packets" 'BEGIN { printf "%.4f", (100*b)/t }')
    else
        pct="0.0000"
    fi

    echo "$day,$total_packets,$bgp_packets,$pct" >> "$OUT"
 done

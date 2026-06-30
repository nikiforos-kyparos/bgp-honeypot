import os
import time
import json
import requests
import pandas as pd

INPUT_CSV = "bgp_open_ip_reported_asn_by_day.csv"
OUTPUT_CSV = "bgp_open_cumulative_asns.csv"
CACHE_FILE = "ipinfo_asn_cache.json"

YEAR = 2026

IPINFO_TOKEN = os.getenv("IPINFO_TOKEN")

df = pd.read_csv(INPUT_CSV)

df["date_parsed"] = pd.to_datetime(
df["date"] + f"/{YEAR}",
format="%d/%m/%Y"
)

df = df.sort_values("date_parsed")

#Load cache

if os.path.exists(CACHE_FILE):
with open(CACHE_FILE, "r") as f:
ip_cache = json.load(f)
else:
ip_cache = {}

def lookup_real_asn(ip: str):
if ip in ip_cache:
return ip_cache[ip]

url = f"https://ipinfo.io/{ip}/json"
params = {"token": IPINFO_TOKEN}

try:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    org = data.get("org", "")

    real_asn = None
    if org.startswith("AS"):
        real_asn = org.split()[0].replace("AS", "")

    ip_cache[ip] = real_asn

    time.sleep(0.1)

    return real_asn

except Exception as e:
    print(f"Lookup failed for {ip}: {e}")
    ip_cache[ip] = None
    return None

#Lookup real ASN only once per unique IP

unique_ips = sorted(df["src_ip"].dropna().unique())

for i, ip in enumerate(unique_ips, start=1):
lookup_real_asn(ip)

if i % 50 == 0:
    with open(CACHE_FILE, "w") as f:
        json.dump(ip_cache, f, indent=2)

with open(CACHE_FILE, "w") as f:
json.dump(ip_cache, f, indent=2)

df["real_asn"] = df["src_ip"].map(ip_cache)

seen_reported_asns = set()
seen_real_asns = set()

rows = []

for date, group in df.groupby("date_parsed"):
daily_reported_asns = set(
group["reported_asn"]
.dropna()
.astype(str)
)

daily_real_asns = set(
    group["real_asn"]
    .dropna()
    .astype(str)
)

seen_reported_asns.update(daily_reported_asns)
seen_real_asns.update(daily_real_asns)

rows.append({
    "date": date.strftime("%d/%m"),
    "daily_unique_reported_asns": len(daily_reported_asns),
    "daily_unique_real_asns": len(daily_real_asns),
    "cumulative_unique_reported_asns": len(seen_reported_asns),
    "cumulative_unique_real_asns": len(seen_real_asns),
})

out = pd.DataFrame(rows)
out.to_csv(OUTPUT_CSV, index=False)

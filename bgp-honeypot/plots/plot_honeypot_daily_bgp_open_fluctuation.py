import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

csv_file = "bgp_open_cumulative_unique_ips.csv"
YEAR = 2026

df = pd.read_csv(csv_file)

df["date"] = pd.to_datetime(
    df["date"] + f"/{YEAR}",
    format="%d/%m/%Y"
)

df = df.sort_values("date")

plt.figure(figsize=(15, 8))

plt.plot(
    df["date"].values,
    df["daily_total_open_packets"].values,
    label="Daily Total BGP OPEN Packets",
    linewidth=2.5,
    marker="o",
    markersize=4
)

plt.plot(
    df["date"].values,
    df["daily_unique_ips"].values,
    label="Daily Unique Source IPs",
    linewidth=2.5,
    marker="s",
    markersize=4
)

ax = plt.gca()

ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))

plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)

plt.xlabel("Deployment Day", fontsize=13)
plt.ylabel("Daily Count", fontsize=13)

plt.title(
    "Daily Fluctuation of BGP OPEN Activity During Honeypot Deployment",
    fontsize=17,
    pad=20
)

plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(fontsize=11, frameon=True)

plt.tight_layout()

plt.savefig("honeypot_daily_bgp_open_fluctuation.pdf", bbox_inches="tight")
plt.savefig("honeypot_daily_bgp_open_fluctuation.png", dpi=300, bbox_inches="tight")

plt.show()

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

df["cumulative_total_open_packets"] = df["daily_total_open_packets"].cumsum()

plt.figure(figsize=(15, 8))

plt.plot(
    df["date"].values,
    df["cumulative_total_open_packets"].values,
    label="Cumulative Total BGP OPEN Packets",
    linewidth=2.8,
    marker="o",
    markersize=4
)

plt.plot(
    df["date"].values,
    df["cumulative_unique_ips"].values,
    label="Cumulative Unique Source IPs",
    linewidth=2.8,
    marker="s",
    markersize=4
)

ax = plt.gca()

ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))

plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)

plt.xlabel("Deployment Day", fontsize=13)
plt.ylabel("Cumulative Count", fontsize=13)

plt.title(
    "Cumulative Growth of BGP OPEN Activity During Honeypot Deployment",
    fontsize=17,
    pad=20
)

plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(fontsize=11, frameon=True)

plt.annotate(
    f"{df['cumulative_total_open_packets'].iloc[-1]}",
    (
        df["date"].values[-1],
        df["cumulative_total_open_packets"].values[-1]
    ),
    textcoords="offset points",
    xytext=(8, 0),
    fontsize=10
)

plt.annotate(
    f"{df['cumulative_unique_ips'].iloc[-1]}",
    (
        df["date"].values[-1],
        df["cumulative_unique_ips"].values[-1]
    ),
    textcoords="offset points",
    xytext=(8, -12),
    fontsize=10
)

plt.tight_layout()

plt.savefig("honeypot_bgp_open_cumulative_growth.pdf", bbox_inches="tight")
plt.savefig("honeypot_bgp_open_cumulative_growth.png", dpi=300, bbox_inches="tight")

plt.show()

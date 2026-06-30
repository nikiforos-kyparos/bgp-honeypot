import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

csv_file = "bgp_open_cumulative_asns.csv"

YEAR = 2026

df = pd.read_csv(csv_file)

df["date"] = pd.to_datetime(
    df["date"] + f"/{YEAR}",
    format="%d/%m/%Y"
)

df = df.sort_values("date")

df["new_unique_reported_asns"] = df["cumulative_unique_reported_asns"].diff()
df["new_unique_real_asns"] = df["cumulative_unique_real_asns"].diff()

df.loc[df.index[0], "new_unique_reported_asns"] = df.loc[
    df.index[0], "cumulative_unique_reported_asns"
]

df.loc[df.index[0], "new_unique_real_asns"] = df.loc[
    df.index[0], "cumulative_unique_real_asns"
]

df["new_unique_reported_asns"] = df["new_unique_reported_asns"].astype(int)
df["new_unique_real_asns"] = df["new_unique_real_asns"].astype(int)

plt.figure(figsize=(15, 8))

plt.plot(
    df["date"].values,
    df["new_unique_reported_asns"].values,
    label="New Globally Unique Reported ASNs",
    linewidth=2.8,
    marker="o",
    markersize=4
)

plt.plot(
    df["date"].values,
    df["new_unique_real_asns"].values,
    label="New Globally Unique Real ASNs",
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
plt.ylabel("New Unique ASNs Discovered", fontsize=13)

plt.title(
    "Daily Discovery of New Globally Unique Reported and Real ASNs",
    fontsize=17,
    pad=20
)

plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(fontsize=11, frameon=True)

plt.tight_layout()

plt.savefig("honeypot_new_unique_asns_per_day.pdf", bbox_inches="tight")
plt.savefig("honeypot_new_unique_asns_per_day.png", dpi=300, bbox_inches="tight")

plt.show()

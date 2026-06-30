import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

honeypot_df = pd.read_csv("daily_bgp_percentage.csv")
telescope_df = pd.read_csv("daily_bgp_percentage_TELESCOPE.csv")

honeypot_df["date"] = pd.to_datetime(honeypot_df["date"])
telescope_df["day"] = pd.to_datetime(telescope_df["day"])

honeypot_df["bgp_percentage"] = (
    honeypot_df["bgp_percentage"]
    .astype(str)
    .str.replace(",", ".", regex=False)
    .astype(float)
)

telescope_df["bgp_percentage"] = (
    telescope_df["bgp_percentage"]
    .astype(str)
    .str.replace(",", ".", regex=False)
    .astype(float)
)

honeypot_df = honeypot_df.sort_values("date")
telescope_df = telescope_df.sort_values("day")

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    honeypot_df["date"].to_numpy(),
    honeypot_df["bgp_percentage"].to_numpy(),
    marker="o",
    linewidth=2,
    label="BGP Honeypot"
)

ax.plot(
    telescope_df["day"].to_numpy(),
    telescope_df["bgp_percentage"].to_numpy(),
    marker="o",
    linewidth=2,
    label="Reactive Telescope"
)

ax.set_title("Daily Percentage of BGP Traffic")
ax.set_xlabel("Deployment Day")
ax.set_ylabel("BGP Traffic (%)")

ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))

plt.xticks(rotation=45)

plt.grid(True)
plt.legend()

plt.tight_layout()

plt.savefig("daily_bgp_percentage_comparison.png", dpi=300)

plt.show()

#!/usr/bin/env python3

import matplotlib.pyplot as plt


HONEYPOT_SIZE = 129
TELESCOPE_SIZE = 2304

CHECKPOINTS = ["03/04", "22/04", "10/05"]

# Raw cumulative ASN counts at each checkpoint
reported_honeypot = [7, 7, 7]
reported_telescope = [115, 115, 116]

real_honeypot = [16, 20, 23]
real_telescope = [23, 28, 31]


def normalize(values, size):
    return [v / size for v in values]


def plot_normalized_comparison(
    honeypot_values,
    telescope_values,
    title,
    output_file,
):
    honeypot_norm = normalize(honeypot_values, HONEYPOT_SIZE)
    telescope_norm = normalize(telescope_values, TELESCOPE_SIZE)

    plt.figure(figsize=(8, 4.8))

    plt.plot(
        CHECKPOINTS,
        honeypot_norm,
        marker="o",
        linewidth=2,
        label="BGP honeypot",
    )

    plt.plot(
        CHECKPOINTS,
        telescope_norm,
        marker="o",
        linewidth=2,
        label="Reactive telescope",
    )

    plt.xlabel("Collection checkpoint")
    plt.ylabel("Unique ASNs per monitored IP")
    plt.title(title)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()

    plt.savefig(output_file, dpi=300)
    plt.close()


def main():
    plot_normalized_comparison(
        reported_honeypot,
        reported_telescope,
        "Normalized Cumulative Unique Reported ASNs",
        "normalized_reported_asns.png",
    )

    plot_normalized_comparison(
        real_honeypot,
        real_telescope,
        "Normalized Cumulative Unique Real ASNs",
        "normalized_real_asns.png",
    )


if __name__ == "__main__":
    main()

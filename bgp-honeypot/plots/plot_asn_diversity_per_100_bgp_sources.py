#!/usr/bin/env python3

import matplotlib.pyplot as plt


CHECKPOINTS = ["03/04", "22/04", "10/05"]

# Cumulative unique BGP OPEN source IPs at each checkpoint
honeypot_source_ips = [496, 901, 1594]
telescope_source_ips = [2661, 3778, 5019]

# Raw cumulative REPORTED ASN counts at each checkpoint
reported_honeypot = [7, 7, 7]
reported_telescope = [115, 115, 116]

# Raw cumulative REAL ASN counts at each checkpoint
real_honeypot = [16, 20, 23]
real_telescope = [23, 28, 31]


def normalize_by_source_ips(asn_values, source_ip_values):
    return [
        (asn / source_ips) * 100 if source_ips != 0 else 0
        for asn, source_ips in zip(asn_values, source_ip_values)
    ]


def plot_normalized_comparison(
    honeypot_asns,
    telescope_asns,
    title,
    output_file,
):
    honeypot_norm = normalize_by_source_ips(honeypot_asns, honeypot_source_ips)
    telescope_norm = normalize_by_source_ips(telescope_asns, telescope_source_ips)

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
    plt.ylabel("Unique ASNs per 100 BGP OPEN source IPs")
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
        "Reported ASN Diversity per 100 BGP OPEN Source IPs",
        "reported_asns_per_100_bgp_open_source_ips.png",
    )

    plot_normalized_comparison(
        real_honeypot,
        real_telescope,
        "Real ASN Diversity per 100 BGP OPEN Source IPs",
        "real_asns_per_100_bgp_open_source_ips.png",
    )


if __name__ == "__main__":
    main()

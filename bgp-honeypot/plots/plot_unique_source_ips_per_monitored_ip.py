#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "values",
        nargs=6,
        type=float,
    )

    parser.add_argument(
        "--honeypot-size",
        type=float,
        default=128,
    )

    parser.add_argument(
        "--telescope-size",
        type=float,
        default=2048,
    )

    parser.add_argument(
        "--output",
        default="normalized_unique_source_ips.png",
    )

    args = parser.parse_args()

    honeypot_raw = args.values[:3]
    telescope_raw = args.values[3:]

    honeypot_norm = [x / args.honeypot_size for x in honeypot_raw]
    telescope_norm = [x / args.telescope_size for x in telescope_raw]

    checkpoints = ["03/04", "22/04", "10/05"]

    plt.figure(figsize=(8, 4.8))

    plt.plot(
        checkpoints,
        honeypot_norm,
        marker="o",
        linewidth=2,
        label="BGP honeypot",
    )

    plt.plot(
        checkpoints,
        telescope_norm,
        marker="o",
        linewidth=2,
        label="Reactive telescope",
    )

    plt.xlabel("Collection checkpoint")
    plt.ylabel("Cumulative unique source IPs per monitored IP")
    plt.title("Normalized Cumulative Unique Source IPs")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()

    plt.savefig(args.output, dpi=300)
    plt.close()

if __name__ == "__main__":
    main()

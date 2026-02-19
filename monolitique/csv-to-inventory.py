#!/usr/bin/env python3
"""
csv-to-inventory.py
Lit hosts.csv et génère un inventaire ansible initial (tous les hosts dans [all])
pour que cred-checker puisse les tester.
Usage: python3 csv-to-inventory.py --csv hosts.csv --out output/all-hosts.ini
"""
import argparse
import csv
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="hosts.csv")
    parser.add_argument("--out", default="output/all-hosts.ini")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    with open(args.csv, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    with open(args.out, "w") as out:
        out.write("[all]\n")
        for row in rows:
            hostname = row.get("hostname", "").strip()
            ip       = row.get("ip", "").strip()
            if hostname and ip:
                out.write(f"{hostname} ansible_host={ip}\n")

    print(f"Inventaire généré : {args.out} ({len(rows)} hosts)")

if __name__ == "__main__":
    main()

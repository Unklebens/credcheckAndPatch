#!/usr/bin/env python3
"""
csv-to-inventory.py
Lit un fichier CSV sans header obligatoire et génère un inventaire Ansible [all].
Chaque ligne non vide est traitée comme un hostname.
Le DNS interne est utilisé directement — pas de résolution explicite.

Usage: python3 csv-to-inventory.py --csv hosts.csv --out output/all-hosts.ini
"""
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="hosts.csv")
    parser.add_argument("--out", default="output/all-hosts.ini")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    with open(args.csv, newline="") as f:
        rows = [line.strip() for line in f if line.strip()]

    with open(args.out, "w") as out:
        out.write("[all]\n")
        for hostname in rows:
            out.write(f"{hostname}\n")

    print(f"Inventaire brut généré : {args.out} ({len(rows)} hosts)")

if __name__ == "__main__":
    main()

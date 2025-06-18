#!/usr/bin/env python3
import csv
import subprocess
import argparse
import shlex
from datetime import datetime

def import_users(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            username    = row['username']
            pw_hash     = row['password_hash']
            expire_date = row['expiration_date'].strip()  # Format: YYYY-MM-DD oder leer

            # Baue useradd-Befehl
            cmd = ["useradd", "-m", "-p", pw_hash]
            if expire_date:
                # Validierung
                try:
                    datetime.strptime(expire_date, "%Y-%m-%d")
                    cmd += ["-e", expire_date]
                except ValueError:
                    print(f"Warnung: Ungültiges Ablaufdatum '{expire_date}' für {username}, übersprungen.")

            cmd.append(username)

            # Führe den Befehl aus
            print(f"→ Erstelle User: {username}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"   Fehler bei {username}: {result.stderr.strip()}")
            else:
                print(f"   OK")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Importiert Benutzer aus users.csv lokal auf diesem Server."
    )
    parser.add_argument(
        "--csv", "-c",
        default="users.csv",
        help="Pfad zur users.csv (default: users.csv)"
    )
    args = parser.parse_args()

    # Prüfe Root-Rechte
    import os, sys
    if os.geteuid() != 0:
        print("Dieses Skript muss als root ausgeführt werden.")
        sys.exit(1)

    import_users(args.csv)

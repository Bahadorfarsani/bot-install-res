#!/usr/bin/env python3
import csv
import datetime
import os
import sys

SHADOW_FILE = '/etc/shadow'
OUTPUT_CSV = 'users.csv'

def parse_shadow():
    users = []
    epoch = datetime.date(1970, 1, 1)
    with open(SHADOW_FILE, 'r') as f:
        for line in f:
            parts = line.strip().split(':')
            # parts: [username, passwd_hash, lastchg, min, max, warn, inactive, expire, flag]
            if len(parts) < 8:
                continue
            username     = parts[0]
            passwd_hash  = parts[1]
            expire_field = parts[7]

            if expire_field.isdigit():
                # expire_field = Anzahl der Tage seit 1970-01-01, an dem das Konto deaktiviert wird
                expire_days = int(expire_field)
                expire_date = epoch + datetime.timedelta(days=expire_days)
                expire_str  = expire_date.isoformat()
            else:
                expire_str = ''

            users.append((username, passwd_hash, expire_str))
    return users

def write_csv(users):
    with open(OUTPUT_CSV, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['username', 'password_hash', 'expiration_date'])
        writer.writerows(users)
    print(f'Daten erfolgreich exportiert nach: {OUTPUT_CSV}')

if __name__ == '__main__':
    # Prüfen, ob das Skript als root läuft
    if os.geteuid() != 0:
        print('Fehler: Dieses Skript muss als root ausgeführt werden.')
        sys.exit(1)

    users = parse_shadow()
    write_csv(users)

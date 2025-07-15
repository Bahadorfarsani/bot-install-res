import subprocess
import os
import signal
import time
from collections import defaultdict
from datetime import datetime

# Geschützte Benutzer – deren Sessions werden nie beendet
PROTECTED_USERS = ['root', 'ubuntu']
LOGFILE = "/root/killed_sshd_sessions.log"

def log_console(msg):
    """Ausgabe auf Konsole mit Timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {msg}")

def log_to_file(msg):
    """Schreibt Logzeile in Datei /root/killed_sshd_sessions.log"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {msg}\n"
    try:
        with open(LOGFILE, 'a') as f:
            f.write(log_entry)
    except Exception as e:
        log_console(f"⚠️ Fehler beim Schreiben in Logdatei: {e}")

def get_sshd_sessions():
    """
    Sammelt alle sshd-Prozesse (TTY oder nicht), gruppiert nach Benutzer.
    """
    result = subprocess.run(['ps', '-eo', 'pid,ppid,tty,user,comm'], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    user_sessions = defaultdict(list)

    for line in lines[1:]:
        parts = line.split(None, 4)
        if len(parts) != 5:
            continue
        pid, ppid, tty, user, command = parts
        if command == 'sshd':
            user_sessions[user].append({
                'pid': int(pid),
                'ppid': int(ppid),
                'tty': tty,
                'user': user
            })
    return user_sessions

def kill_all_sessions_for_users_with_multiple(user_sessions):
    for user, sessions in user_sessions.items():
        if user in PROTECTED_USERS:
            log_console(f"🔒 Benutzer '{user}' ist geschützt – übersprungen.")
            continue

        if len(sessions) > 1:
            log_console(f"🚫 Benutzer '{user}' hat {len(sessions)} Sessions – ALLE werden beendet.")
            for session in sessions:
                pid = session['pid']
                tty = session['tty']
                try:
                    os.kill(pid, signal.SIGKILL)
                    msg = f"✓ Gekillt: User '{user}', PID {pid}, TTY {tty}"
                    log_console(msg)
                    log_to_file(msg)
                except ProcessLookupError:
                    log_console(f"✗ Prozess {pid} nicht gefunden.")
                except PermissionError:
                    log_console(f"✗ Keine Berechtigung für PID {pid}.")
        else:
            log_console(f"✅ Benutzer '{user}' hat nur eine Session – alles okay.")

def main_loop(interval_seconds=2):
    log_console("🔄 SSHD Session Watcher gestartet.")
    log_to_file("🔄 SSHD Session Watcher gestartet.")
    while True:
        user_sessions = get_sshd_sessions()
        kill_all_sessions_for_users_with_multiple(user_sessions)
        time.sleep(interval_seconds)

if __name__ == '__main__':
    main_loop()




import argparse
import sqlite3
import signal
import subprocess
import time
import os


PID_FILE = os.path.expanduser('~/activity_tracker.pid')


def setup_db():
    db_path = os.path.expanduser('~/activity_tracker.db')
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity(
            id INTEGER PRIMARY KEY,
            window_title TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')

def get_active_window_title():
    window_id = subprocess.check_output(['xdotool', 'getactivewindow']).decode().strip()
    window_name = subprocess.check_output(['xdotool', 'getwindowname', window_id]).decode().strip()
    return window_name
def track_activity(interval):
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))

    try:
        while True:
            window_title = get_active_window_title()
            db_path = os.path.expanduser('~/activity_tracker.db')
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO activity(window_title) VALUES(?)', (window_title,))
            time.sleep(interval)
    except KeyboardInterrupt:
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
        print("\nTracking stopped.")

def stop_tracking():
    if os.path.exists(PID_FILE):
        with open(PID_FILE, 'r') as f:
            pid = int(f.read())
            try:
                os.kill(pid, signal.SIGINT)
            except ProcessLookupError:
                print("Tracking process not found.")
            os.remove(PID_FILE)
        print("Tracking stopped.")
    else:
        print("No tracking process found.")

def main():
    parser = argparse.ArgumentParser(description="Track time spent on software activities.")
    subparsers = parser.add_subparsers(dest='command')
    
    # Setup command
    setup_parser = subparsers.add_parser('setup', help="Set up the SQLite database.")
    
    # Start command
    start_parser = subparsers.add_parser('start', help="Start tracking activity.")
    start_parser.add_argument('-i', '--interval', type=int, default=60, 
                              help="Interval (in seconds) to check active window. Default is 60 seconds.")

    # Stop command
    stop_parser = subparsers.add_parser('stop', help="Stop tracking activity.")
    
    args = parser.parse_args()

    if args.command == 'setup':
        setup_db()
        print("Database setup complete.")

    elif args.command == 'start':
        track_activity(args.interval)

    elif args.command == 'stop':
        stop_tracking()

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
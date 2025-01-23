import sys
import os
import time
import signal
import argparse

PID_FILE = '/tmp/test_project.pid'

def start_daemon():
    """Start the daemon in the background."""
    if os.path.exists(PID_FILE):
        print("Daemon already running. Use restart or stop first.")
        sys.exit(1)

    pid = os.fork()
    if pid > 0:
        # Parent process exits
        print(f"Daemon started with PID {pid}.")
        with open(PID_FILE, 'w') as pid_file:
            pid_file.write(str(pid))
        sys.exit(0)

    # Child process continues
    os.setsid()
    os.umask(0)
    sys.stdout.flush()
    sys.stderr.flush()
    __log = "/tmp/test_project.log"
    with open("/dev/null", "w") as devnull:
        os.dup2(devnull.fileno(), sys.stdin.fileno())
    
    with open(__log, "w") as log:    
        os.dup2(log.fileno(), sys.stdout.fileno())
        os.dup2(log.fileno(), sys.stderr.fileno())

    # Infinite loop for the daemon process
    try:
        while True:
            import deamon_touches
            deamon_touches.main()
            time.sleep(5)
    except KeyboardInterrupt:
        cleanup()


def stop_daemon():
    """Stop the daemon."""
    if not os.path.exists(PID_FILE):
        print("No daemon is currently running.")
        sys.exit(1)

    with open(PID_FILE, 'r') as pid_file:
        pid = int(pid_file.read().strip())

    try:
        os.kill(pid, signal.SIGTERM)
        print("Daemon stopped.")
    except ProcessLookupError:
        print("Process not found. Removing stale PID file.")
    except Exception as e:
        print(f"Error stopping daemon: {e}")
    finally:
        cleanup()


def restart_daemon():
    """Restart the daemon."""
    stop_daemon()
    start_daemon()


def daemon_status():
    """Check the status of the daemon."""
    if os.path.exists(PID_FILE):
        with open(PID_FILE, 'r') as pid_file:
            pid = pid_file.read().strip()
        print(f"Daemon running with PID {pid}.")
    else:
        print("Daemon is not running.")


def cleanup():
    """Clean up the PID file."""
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)


def run_normal_mode():
    """Run the program in normal mode."""
    print("Running in normal mode. Press Ctrl+C to exit.")
    try:
        while True:
            print("Program running...")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Exiting normal mode.")

# Argument parsing
parser = argparse.ArgumentParser(description="Test project: daemon and normal modes.")
subparsers = parser.add_subparsers(dest="mode")

# Subparser for normal mode
parser_load = subparsers.add_parser("load", help="Run in normal mode.")

# Subparser for daemon mode
parser_daemon = subparsers.add_parser("daemon", help="Run as a daemon.")
parser_daemon.add_argument("action", choices=["start", "stop", "restart", "status"], help="Action for the daemon.")

if __name__ == "__main__":
    args = parser.parse_args()

    if args.mode == "load":
        run_normal_mode()
    elif args.mode == "daemon":
        if args.action == "start":
            start_daemon()
        elif args.action == "stop":
            stop_daemon()
        elif args.action == "restart":
            restart_daemon()
        elif args.action == "status":
            daemon_status()
    else:
        parser.print_help()

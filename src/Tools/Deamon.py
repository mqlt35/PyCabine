

class Deamon:
    __log = "/tmp/my_thread_daemon.log"
    __pid_file = "/tmp/my_thread_daemon.pid"
    __scenario = None
    __action = None
    def __init__(self, api):
        import os
        import sys
        import time
        import signal
        print("Classe Deamon initialisée")
        self.__api = api
        self.__os = os
        self.__sys = sys
        self.__time = time
        self.__signal = signal

    def set_options(self, options):
        self.__pid_file = options.pidfile
        self.__scenario = options.scenario
        self.__action = options.action

    def start_daemon(self):
        """Start the daemon."""
        if self.__os.path.exists(self.__pid_file):
            print("Daemon already running. Use restart or stop first.")
            self.__sys.exit(1)

        pid = self.__os.fork()
        if pid > 0:
            # Parent process exits
            print(f"Daemon started with PID {pid}.")
            with open(self.__pid_file, 'w') as pid_file:
                pid_file.write(str(pid))
            self.__sys.exit(0)

        print(self.__os.getpid())
        self.__os.setsid()
        self.__os.umask(0)
        self.__sys.stdout.flush()
        self.__sys.stderr.flush()
        print("Starting daemon...")
        with open("/dev/null", "w") as devnull:
            self.__os.dup2(devnull.fileno(), self.__sys.stdin.fileno())
        
        print("Youhou")
        with open(self.__log, "w") as log:    
            self.__os.dup2(log.fileno(), self.__sys.stdout.fileno())
            self.__os.dup2(log.fileno(), self.__sys.stderr.fileno())

        self.__signal.signal(self.__signal.SIGTERM, self.signal_handler)
        self.__signal.signal(self.__signal.SIGINT, self.signal_handler)  
        # Infinite loop for the daemon process
        try:
            self.__api.RunScenario(self.__scenario)
        except KeyboardInterrupt:
            print("Daemon interrupted.")
            self.__api.StopRunningScenario()
            self.cleanup()

    def signal_handler(self, signum, frame):
        print(f"Received signal {signum}, stopping daemon...")
        self.__api.StopRunningScenario()
        self.cleanup()
        self.__sys.exit(0)

    def stop_daemon(self):
        """Stop the daemon."""
        if not self.__os.path.exists(self.__pid_file):
            print("No daemon is currently running.")
            self.__sys.exit(1)

        with open(self.__pid_file, 'r') as pid_file:
            pid = int(pid_file.read().strip())
        
        #self.__os.kill(pid, self.__signal.SIGTERM)
    
        try:
            self.__os.kill(pid, self.__signal.SIGTERM)
            print("Daemon stopped.")
        except ProcessLookupError:
            print("Process not found. Removing stale PID file.")
        except Exception as e:
            print(f"Error stopping daemon: {e}")
        finally:
            self.cleanup()

        

    def restart_daemon(self):
        """Restart the daemon."""
        self.stop_daemon()
        self.start_daemon()

    def daemon_status(self):
        """Check the status of the daemon."""
        if self.__os.path.exists(self.__pid_file):
            with open(self.__pid_file, 'r') as pid_file:
                pid = pid_file.read().strip()
            print(f"Daemon running with PID {pid}.")
        else:
            print("Daemon is not running.")

    def cleanup(self):
        """Clean up the PID file."""
        if self.__os.path.exists(self.__pid_file):
            self.__os.remove(self.__pid_file)

    
    def manage_daemon(self):
        """Gère les actions : start, stop, restart, status."""
        if self.__action == "start":
            self.start_daemon()
        elif self.__action == "stop":
            self.stop_daemon()
        elif self.__action == "restart":
            self.restart_daemon()
        elif self.__action == "status":
            self.daemon_status()
        else:
            raise Exception(f"Action '{self.__action}' non reconnue. Utilisez : start, stop, restart, status.")


def init(api):
    return Deamon(api)
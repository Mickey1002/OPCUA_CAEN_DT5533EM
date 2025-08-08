# main.py
import time
from Server_files.opcua_server import run_server

def main():
    server = run_server()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Zatrzymywanie serwera...")
        server.stop()

if __name__ == "__main__":
    main()

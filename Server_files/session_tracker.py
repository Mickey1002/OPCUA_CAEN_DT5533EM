import time

def track_sessions(server, interval=1.0):
    """
    Regularly checks the number of active OPC UA clients,
    updates the server variable, and prints it to the console.
    """
    while True:
        try:
            count = len(server.bserver.clients)
            print(f"[session_tracker] Number of clients: {count}")
        except Exception as e:
            print(f"[session_tracker] Error reading sessions: {e}")
        time.sleep(interval)
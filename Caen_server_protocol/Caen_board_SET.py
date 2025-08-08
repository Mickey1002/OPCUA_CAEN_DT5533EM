import time

def board_set_loop(board_set_vars, caen_container, lock, caen_connected_var):
    POLL_INTERVAL = 5
    was_connected = False

    while True:
        connected = caen_connected_var.get_value()
        caen_instance = caen_container.get("instance", None)

        if not connected or caen_instance is None:
            if was_connected:
                print("⚠️ Lost connection to CAEN (BDCLR setter).")
            was_connected = False
            time.sleep(POLL_INTERVAL)
            continue

        if not was_connected:
            print("✅ CAEN connection established (BDCLR setter).")
            was_connected = True

        val = board_set_vars["BDCLR"].get_value()
        if val:
            print("⚙️ BDCLR is True — clearing alarms and resetting flag.")
            with lock:
                caen_instance.query(CMD='SET', PAR='BDCLR')
            board_set_vars["BDCLR"].set_value(False)

        time.sleep(POLL_INTERVAL)
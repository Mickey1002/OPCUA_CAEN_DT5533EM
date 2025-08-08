import time

# Parameters to monitor
board_monitor_params = [
    "BDILK", "BDNCH", "BDNAME", "BDSNUM",
    "BDFREL", "BDALARM", "MACADDR", "IPADDR",
    "SUBMASK", "GATEWAY", "DHCPEN"
]

# Parameters that are strings
STRING_PARAMS = {"BDILK", "BDNAME", "MACADDR", "IPADDR", "SUBMASK", "GATEWAY", "DHCPEN"}

def board_monitor_loop(board_vars, caen_container, lock, caen_connected_var):
    POLL_INTERVAL = 5
    was_connected = False

    while True:
        connected = caen_connected_var.get_value()
        caen_instance = caen_container.get("instance", None)

        if not connected or caen_instance is None:
            if was_connected:
                print("⚠️ Lost connection to CAEN (board monitor) — suspending reads.")
            was_connected = False
            time.sleep(POLL_INTERVAL)
            continue

        if not was_connected:
            print("✅ CAEN connection established (board monitor), starting reads...")
            was_connected = True

        print("\n🛠️ === BOARD PARAMETERS READ ===")
        for param in board_monitor_params:
            try:
                with lock:
                    response = caen_instance.query(CMD='MON', PAR=param)

                if "VAL:" not in response:
                    raise ValueError(f"'VAL:' missing in response: {response}")

                val = response.split("VAL:")[-1].strip().rstrip(";")

                if param in STRING_PARAMS:
                    board_vars[param].set_value(val)
                    print(f"🔧 {param}: \"{val}\"")
                else:
                    try:
                        board_vars[param].set_value(float(val))
                        print(f"🔧 {param}: {float(val)}")
                    except:
                        board_vars[param].set_value(val)
                        print(f"🔧 {param}: \"{val}\" (fallback)")

            except Exception as e:
                print(f"[ERROR] Read error for {param}: {e}")

        print("🛠️ === END OF BOARD READ ===\n")
        time.sleep(POLL_INTERVAL)

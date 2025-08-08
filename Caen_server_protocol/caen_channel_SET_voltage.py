import time
from Caen_config.CAEN_config import NUM_CHANNELS, DEVICE_IP, TIMEOUT
from CAENpy.CAENDesktopHighVoltagePowerSupply import CAENDesktopHighVoltagePowerSupply
from Caen_server_protocol.caen_set_ranges import check_VSET

def setter_voltage_loop(set_vars, server_error_var, caen_container, lock, caen_connected_var):
    POLL_INTERVAL = 1

    was_connected = False
    last_vals = {ch: None for ch in range(NUM_CHANNELS)}

    while True:
        connected = caen_connected_var.get_value()
        caen_instance = caen_container.get("instance", None)

        if not connected or caen_instance is None:
            if was_connected:
                print("⚠️ Lost connection to CAEN or no instance — setter paused.")
            was_connected = False
            time.sleep(POLL_INTERVAL)
            continue

        if not was_connected:
            print("✅ CAEN connection restored, turning off channels and initializing setter.")
            try:
                with lock:
                    for ch in range(NUM_CHANNELS):
                        caen_instance.set_single_channel_parameter(parameter='OFF', channel=ch, value=1)
                        time.sleep(0.5)
                time.sleep(5)
                last_vals = {ch: None for ch in range(NUM_CHANNELS)}
                was_connected = True
            except Exception as e:
                print(f"[ERROR] Error initializing channels after connection: {e}")
                try:
                    if hasattr(caen_instance, "disconnect"):
                        caen_instance.disconnect()
                except Exception:
                    pass
                try:
                    caen_container["instance"] = CAENDesktopHighVoltagePowerSupply(ip=DEVICE_IP)
                    print("🔄 CAEN connection re-established")
                    was_connected = True
                except Exception as e2:
                    print(f"[ERROR] Failed to reconnect: {e2}")
                    was_connected = False
                    caen_container["instance"] = None  # clear instance in case of error

        # If connection is active and initialization succeeded
        for ch in range(NUM_CHANNELS):
            try:
                error_msg = check_VSET(set_vars[ch], ch, server_error_var)
                if error_msg is not None:
                    print(f"[ERROR] {error_msg} - skipping voltage setting on channel {ch}")

                    # Fetch current value from CAEN device and overwrite OPC UA VSET variable
                    try:
                        raw_val = caen_instance.get_single_channel_parameter('VSET', ch)
                        current_val = float(str(raw_val).strip().replace(";", ""))
                        print(f"🔄 Overwriting CH{ch} VSET with value from CAEN: {current_val}")
                        set_vars[ch]['VSET'].set_value(current_val)
                    except Exception as e:
                        print(f"[ERROR] Failed to fetch and overwrite VSET for channel {ch}: {e}")

                    continue  # skip setting voltage on this channel

                val = set_vars[ch]['VSET'].get_value()
                if last_vals[ch] != val:
                    print(f"🔧 Setting channel {ch} VSET to {val}")
                    with lock:
                        caen_instance.set_single_channel_parameter('VSET', ch, val)
                        caen_instance.set_single_channel_parameter('ON', ch, 1)
                    last_vals[ch] = val
            except Exception as e:
                print(f"[ERROR] Setter channel {ch}: {e}")

        time.sleep(POLL_INTERVAL)




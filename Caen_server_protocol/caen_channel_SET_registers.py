import time
from Caen_config.CAEN_config import NUM_CHANNELS, DEVICE_IP, CAEN_PORT
from CAENpy.CAENDesktopHighVoltagePowerSupply import CAENDesktopHighVoltagePowerSupply

from Caen_server_protocol.caen_set_ranges import check_ISET, check_IMRANGE, check_RUP, check_RDW, check_PDWN

def caen_setter_loop(set_vars, server_error_var, caen_container, lock, caen_connected_var):
    POLL_INTERVAL = 1  # Time between polling cycles (in seconds)
    was_connected = False  # Tracks previous connection state to detect changes

    # Initialize last known values for each parameter on each channel
    last_vals = {
        ch: {
            "ISET": None,
            "IMRANGE": None,
            "RUP": None,
            "RDW": None,
            "PDWN": None,
            "MAXV": None,
            "ON": None,
            "OFF": None
        } for ch in range(NUM_CHANNELS)
    }

    # Mapping parameters to their respective validation functions
    check_funcs = {
        "ISET": check_ISET,
        "IMRANGE": check_IMRANGE,
        "RUP": check_RUP,
        "RDW": check_RDW,
        "PDWN": check_PDWN,
    }

    while True:
        connected = caen_connected_var.get_value()  # Check if CAEN device is connected
        caen_instance = caen_container.get("instance", None)  # Get CAEN device instance

        if not connected or caen_instance is None:
            if was_connected:
                print("⚠️ Lost connection to CAEN — setter paused.")
            was_connected = False
            time.sleep(POLL_INTERVAL)
            continue  # Wait and retry if disconnected

        if not was_connected:
            print("✅ Connection to CAEN established — starting setter.")
            was_connected = True

        for ch in range(NUM_CHANNELS):
            try:
                ch_vars = set_vars[ch]

                # Loop through parameters to set (with validation)
                for param in ["ISET", "IMRANGE", "RUP", "RDW", "PDWN", "MAXV"]:
                    try:
                        val = ch_vars[param].get_value()

                        # Only update if value changed since last set
                        if last_vals[ch][param] != val:
                            check_func = check_funcs.get(param)
                            error_msg = None

                            # Run validation if available
                            if check_func is not None:
                                error_msg = check_func(ch_vars, ch, server_error_var)

                            if error_msg is None:
                                print(f"🔧 CH{ch} → {param} = {val}")
                                with lock:
                                    caen_instance.set_single_channel_parameter(param, ch, val)
                                last_vals[ch][param] = val
                            else:
                                print(f"[ERROR] {error_msg} - skipping setting {param} on channel {ch}")
                                try:
                                    # Retrieve current CAEN value to overwrite invalid client input
                                    raw_val = caen_instance.get_single_channel_parameter(param, ch)
                                    current_val = float(str(raw_val).strip().replace(";", ""))
                                    print(f"🔄 Overwriting CH{ch} {param} with value from CAEN: {current_val}")
                                    ch_vars[param].set_value(current_val)
                                    last_vals[ch][param] = current_val
                                except Exception as e:
                                    print(f"[ERROR] Failed to retrieve and overwrite {param} for CH{ch}: {e}")
                    except Exception as e:
                        print(f"[ERROR] Error setting {param} for CH{ch}: {e}")

                # Handle ON/OFF mutually exclusive states
                on_val = ch_vars["ON"].get_value()
                off_val = ch_vars["OFF"].get_value()

                if on_val != last_vals[ch]["ON"] and on_val:
                    print(f"⚙️ CH{ch} → ON = True → OFF = False")
                    with lock:
                        caen_instance.set_single_channel_parameter("ON", ch, True)
                        caen_instance.set_single_channel_parameter("OFF", ch, False)
                    ch_vars["OFF"].set_value(False)
                    last_vals[ch]["ON"] = True
                    last_vals[ch]["OFF"] = False

                elif off_val != last_vals[ch]["OFF"] and off_val:
                    print(f"⚙️ CH{ch} → OFF = True → ON = False")
                    with lock:
                        caen_instance.set_single_channel_parameter("OFF", ch, True)
                        caen_instance.set_single_channel_parameter("ON", ch, False)
                    ch_vars["ON"].set_value(False)
                    last_vals[ch]["OFF"] = True
                    last_vals[ch]["ON"] = False

            except Exception as e:
                print(f"[ERROR] Setter channel {ch}: {e}")

        time.sleep(POLL_INTERVAL)  # Wait before next polling cycle

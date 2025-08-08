import time
from Caen_config.CAEN_config import NUM_CHANNELS, DEVICE_IP
from CAENpy.CAENDesktopHighVoltagePowerSupply import CAENDesktopHighVoltagePowerSupply

def monitoring_float_loop(monitoring_vars, caen_container, lock, caen_connected_var):
    POLL_INTERVAL = 5
    
    monitoring_params = [
        "VSRES", "VSDEC", "VMAX", "VMIN", "VMON",
        "VMRES", "VMDEC", "ISRES", "IMAXH", "IMAXL",
        "IMIN", "ISDEC", "IMON", "IMRESL", "IMRESH",
        "IMDECL", "IMDECH", "MAXV", "MVMIN", "MVMAX", "MVRES",
        "MVDEC", "POL", "STAT", "RUPMIN", "RUPMAX",
        "RUPRES", "RUPDEC", "RDWMIN", "RDWMAX", "RDWRES",
        "RDWDEC", "TRIP", "TRIPMIN", "TRIPMAX", "TRIPRES", "TRIPDEC"
    ]

    STRING_PARAMS = {"POL"}
    was_connected = False

    while True:
        connected = caen_connected_var.get_value()
        caen_instance = caen_container.get("instance", None)

        if not connected or caen_instance is None:
            if was_connected:
                print("⚠️ Lost connection to CAEN or no instance — pausing reads.")
            was_connected = False
            time.sleep(POLL_INTERVAL)
            continue

        # If connection is OK
        if not was_connected:
            print("✅ CAEN connection established, starting reads...")
            was_connected = True

        print("\n📊 === START OF READOUT ===")
        for ch in range(NUM_CHANNELS):
            for param in monitoring_params:
                try:
                    with lock:
                        val = caen_instance.get_single_channel_parameter(param, ch)

                    if param in STRING_PARAMS and isinstance(val, str):
                        val_clean = val.strip().rstrip(';')
                        monitoring_vars[ch][param].set_value(val_clean)
                        print(f"Channel {ch} - {param}: \"{val_clean}\"")
                    else:
                        try:
                            val_float = float(val)
                            monitoring_vars[ch][param].set_value(val_float)
                            print(f"Channel {ch} - {param}: {val_float}")
                        except Exception:
                            val_str = str(val).strip().rstrip(';')
                            monitoring_vars[ch][param].set_value(val_str)
                            print(f"Channel {ch} - {param}: \"{val_str}\"")
                except Exception as e:
                    print(f"[ERROR] Channel {ch} - {param}: {e}")
        print("📊 === END OF READOUT ===\n")

        time.sleep(POLL_INTERVAL)


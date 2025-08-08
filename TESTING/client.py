from opcua import Client

def run_client():
    url = "opc.tcp://192.168.0.10:4840/freeopcua/server/"
    client = Client(url)

    NUM_CHANNELS = 4

    # List of parameters to monitor on each channel
    monitoring_params = [
        "VSET", "VSRES", "VSDEC", "VMAX", "VMIN", "VMON",
        "VMRES", "VMDEC", "ISET", "ISRES", "IMAXH", "IMAXL",
        "IMIN", "ISDEC", "IMON", "IMRANGE", "IMRESL", "IMRESH",
        "IMDECL", "IMDECH", "MAXV", "MVMIN", "MVMAX", "MVRES",
        "MVDEC", "PDWN", "POL", "STAT", "RUP", "RUPMIN", "RUPMAX",
        "RUPRES", "RUPDEC", "RDW", "RDWMIN", "RDWMAX", "RDWRES",
        "RDWDEC", "TRIP", "TRIPMIN", "TRIPMAX", "TRIPRES", "TRIPDEC"
    ]

    try:
        client.connect()
        print(f"Connected to OPC UA server: {url}")

        # Get the root objects node and then the specific device node
        objects = client.get_objects_node()
        device = objects.get_child(["2:MyDevice"])  # Namespace 2, device name

        print("Available commands:")
        print("  SET - set voltage on channel (interactive)")
        print("  READ - display status of all monitored parameters")
        print("  Q - quit")

        while True:
            cmd = input("\nEnter command (SET/READ/Q): ").strip().upper()

            if cmd == "Q":
                print("Exiting client...")
                break

            elif cmd == "SET":
                while True:
                    ch_str = input(f"Enter channel number (0 - {NUM_CHANNELS-1}), or Q to exit SET: ").strip()
                    if ch_str.upper() == "Q":
                        break
                    if not ch_str.isdigit():
                        print("❌ Invalid channel number.")
                        continue
                    ch_num = int(ch_str)
                    if ch_num < 0 or ch_num >= NUM_CHANNELS:
                        print("❌ Channel number out of range.")
                        continue
                    val_str = input(f"Enter voltage value for channel {ch_num}: ").strip()
                    try:
                        voltage = float(val_str)
                    except ValueError:
                        print("❌ Invalid voltage value.")
                        continue

                    try:
                        var_name = f"2:CH{ch_num}_VSET"
                        hv_var = device.get_child([var_name])
                        hv_var.set_value(voltage)
                        print(f"✅ Set channel {ch_num} voltage to {voltage} V")
                    except Exception as e:
                        print(f"❌ Error setting value: {e}")

            elif cmd == "READ":
                print("\n📊 Status of all monitored parameters:")
                for ch_num in range(NUM_CHANNELS):
                    print(f"\n-- Channel {ch_num} --")
                    for param in monitoring_params:
                        try:
                            mon_var_name = f"2:CH{ch_num}_{param}"
                            mon_var = device.get_child([mon_var_name])
                            value = mon_var.get_value()
                            print(f"  {param}: {value}")
                        except Exception as e:
                            print(f"  [!] Error reading {param}: {e}")

            else:
                print("Unknown command. Available commands: SET, READ, Q")

    except KeyboardInterrupt:
        print("\nClosing client...")
    except Exception as e:
        print(f"[ERROR] OPC UA client error: {e}")
    finally:
        client.disconnect()
        print("Disconnected from server.")

if __name__ == "__main__":
    run_client()

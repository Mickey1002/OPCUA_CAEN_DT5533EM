import subprocess
import time
from Caen_config.CAEN_config import CAEN_PORT, DEVICE_IP
from CAENpy.CAENDesktopHighVoltagePowerSupply import CAENDesktopHighVoltagePowerSupply

def ping_host(host, timeout=1000):
    """
    Performs a ping to the host.
    Timeout is in ms for Windows, and in seconds for Linux.
    Returns True if the host responds, False otherwise.
    """
    import platform
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    if platform.system().lower() == 'windows':
        command = ['ping', param, '1', '-w', str(timeout), host]
    else:
        command = ['ping', param, '1', '-W', str(int(timeout / 1000)), host]

    try:
        output = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output.returncode == 0
    except Exception as e:
        print(f"[ping_host] Error pinging {host}: {e}")
        return False


def connection_check_loop(host, port, caen_connected_var, caen_container, interval=5.0):
    """
    Loop that checks connection to CAEN by pinging and updates caen_connected_var accordingly.
    Creates a new CAEN instance if host is reachable but the instance does not yet exist.
    """
    while True:
        if ping_host(host):
            print(f"[connection_check] Ping to CAEN {host} — OK")

            if caen_container.get("instance") is None:
                print("[connection_check] No instance found — attempting to create a new one...")
                try:
                    caen_container["instance"] = CAENDesktopHighVoltagePowerSupply(ip=host)
                    print("[connection_check] CAEN instance created successfully.")
                    caen_connected_var.set_value(True)
                except Exception as e:
                    print(f"[connection_check] ❌ Failed to create CAEN instance: {e}")
                    caen_container["instance"] = None
                    caen_connected_var.set_value(False)
            else:
                caen_connected_var.set_value(True)
        else:
            print(f"[connection_check] Ping to CAEN {host} failed.")
            caen_connected_var.set_value(False)
            caen_container["instance"] = None  # Clear instance on connection loss

        time.sleep(interval)

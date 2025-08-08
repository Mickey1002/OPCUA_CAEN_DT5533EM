import threading
import time
from opcua import Server, ua
from CAENpy.CAENDesktopHighVoltagePowerSupply import CAENDesktopHighVoltagePowerSupply
from Caen_config.CAEN_config import NUM_CHANNELS, DEVICE_IP, CAEN_PORT
from Server_files.Server_config import SERVER_IP, SERVER_PORT

## Server variables
from Server_variables.variable_set_creation import create_register_variables
from Server_variables.variable_monitor_creation import create_monitoring_variables
from Server_variables.variables_server import create_caen_server_variable
from Server_variables.variable_board import create_board_mon_variables
from Server_variables.variable_board import create_board_set_variables

## Caen functions
from Caen_config.CAEN_SET_config import initialize_register_variables
from Caen_server_protocol.caen_channel_monitor import monitoring_float_loop
from Caen_server_protocol.caen_channel_SET_voltage import setter_voltage_loop
from Caen_server_protocol.Caen_board_connection_check import connection_check_loop
from Caen_server_protocol.Caen_board_monitor import board_monitor_loop  
from Caen_server_protocol.Caen_board_SET import board_set_loop
from Caen_server_protocol.caen_channel_SET_registers import caen_setter_loop

## Server monitoring
from Server_files.session_tracker import track_sessions
from Server_files.Session_errors import set_server_error

def run_server():
    server = Server()
    endpoint = f"opc.tcp://{SERVER_IP}:{SERVER_PORT}/freeopcua/server/"
    server.set_endpoint(endpoint)
    server.set_security_policy([ua.SecurityPolicyType.NoSecurity])

    uri = "http://example.org"
    idx = server.register_namespace(uri)

    objects = server.get_objects_node()
    device = objects.add_object(idx, "MyDevice")

    ## Initialization of server variables
    set_vars = create_register_variables(device, idx, NUM_CHANNELS)
    monitoring_vars = create_monitoring_variables(device, idx, NUM_CHANNELS)
    board_mon_vars = create_board_mon_variables(device, idx) 
    board_set_vars = create_board_set_variables(device, idx) 
    caen_connected_var, server_error_var = create_caen_server_variable(device, idx)
    
    ## Default setup of CAEN registers
    initialize_register_variables(set_vars)
    
    set_server_error(server_error_var, "NONE")

    caen_container = {"instance": None}
    caen_lock = threading.Lock()

    server.start()
    print("OPC UA server running at opc.tcp://192.168.0.10:4840/freeopcua/server/")

    threading.Thread(
        target=track_sessions,
        args=(server,),
        daemon=True
    ).start()

    threading.Thread(
        target=connection_check_loop,
        args=(DEVICE_IP, CAEN_PORT, caen_connected_var, caen_container),
        daemon=True
    ).start()

    threading.Thread(
        target=monitoring_float_loop,
        args=(monitoring_vars, caen_container, caen_lock, caen_connected_var),
        daemon=True
    ).start()

    threading.Thread(
        target=setter_voltage_loop,
        args=(set_vars, server_error_var, caen_container, caen_lock, caen_connected_var),
        daemon=True
    ).start()

    threading.Thread(
        target=caen_setter_loop,
        args=(set_vars, server_error_var, caen_container, caen_lock, caen_connected_var),
        daemon=True
    ).start()

    threading.Thread(  
        target=board_monitor_loop,
        args=(board_mon_vars, caen_container, caen_lock, caen_connected_var),
        daemon=True
    ).start()

    threading.Thread(  
        target=board_set_loop,
        args=(board_set_vars, caen_container, caen_lock, caen_connected_var),
        daemon=True
    ).start()

    return server


from Server_files.Session_errors import set_server_error
from Caen_config.Caen_ranges_definition import RANGES, VALID_IMRANGE, VALID_PDWN

def check_VSET(vars_dict, channel, server_error_var):
    node = vars_dict.get('VSET')
    range_min, range_max = RANGES["VSET"]
    if node is None:
        return None
    try:
        val = node.get_value()
        if val < range_min:
            msg = f"CH{channel} VSET = {val} below minimum {range_min}"
            set_server_error(server_error_var, msg)
            return msg
        elif val > range_max:
            msg = f"CH{channel} VSET = {val} above maximum {range_max}"
            set_server_error(server_error_var, msg)
            return msg
    except Exception as e:
        msg = f"CH{channel} VSET read error: {str(e)}"
        set_server_error(server_error_var, msg)
        return msg
    return None

def check_ISET(vars_dict, channel, server_error_var):
    node = vars_dict.get('ISET')
    range_min, range_max = RANGES["ISET"]
    if node is None:
        return
    try:
        val = node.get_value()
        if val < range_min:
            msg = f"CH{channel} ISET = {val} below minimum {range_min}"
            set_server_error(server_error_var, msg)
        elif val > range_max:
            msg = f"CH{channel} ISET = {val} above maximum {range_max}"
            set_server_error(server_error_var, msg)
    except Exception as e:
        msg = f"CH{channel} ISET read error: {str(e)}"
        set_server_error(server_error_var, msg)

def check_RUP(vars_dict, channel, server_error_var):
    node = vars_dict.get('RUP')
    range_min, range_max = RANGES["RUP"]
    if node is None:
        return
    try:
        val = node.get_value()
        if val < range_min:
            msg = f"CH{channel} RUP = {val} below minimum {range_min}"
            set_server_error(server_error_var, msg)
        elif val > range_max:
            msg = f"CH{channel} RUP = {val} above maximum {range_max}"
            set_server_error(server_error_var, msg)
    except Exception as e:
        msg = f"CH{channel} RUP read error: {str(e)}"
        set_server_error(server_error_var, msg)

def check_RDW(vars_dict, channel, server_error_var):
    node = vars_dict.get('RDW')
    range_min, range_max = RANGES["RDW"]
    if node is None:
        return
    try:
        val = node.get_value()
        if val < range_min:
            msg = f"CH{channel} RDW = {val} below minimum {range_min}"
            set_server_error(server_error_var, msg)
        elif val > range_max:
            msg = f"CH{channel} RDW = {val} above maximum {range_max}"
            set_server_error(server_error_var, msg)
    except Exception as e:
        msg = f"CH{channel} RDW read error: {str(e)}"
        set_server_error(server_error_var, msg)

def check_IMRANGE(vars_dict, channel, server_error_var):
    node = vars_dict.get('IMRANGE')
    if node is None:
        return
    try:
        val = node.get_value()
        if val not in VALID_IMRANGE:
            msg = f"CH{channel} IMRANGE = '{val}' invalid (must be LOW or HIGH)"
            set_server_error(server_error_var, msg)
    except Exception as e:
        msg = f"CH{channel} IMRANGE read error: {str(e)}"
        set_server_error(server_error_var, msg)

def check_PDWN(vars_dict, channel, server_error_var):
    node = vars_dict.get('PDWN')
    if node is None:
        return
    try:
        val = node.get_value()
        if val not in VALID_PDWN:
            msg = f"CH{channel} PDWN = '{val}' invalid (must be RAMP or KILL)"
            set_server_error(server_error_var, msg)
    except Exception as e:
        msg = f"CH{channel} PDWN read error: {str(e)}"
        set_server_error(server_error_var, msg)

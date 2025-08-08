from opcua import ua

def create_register_variables(device, idx, num_channels):
    set_vars = {}
    for ch in range(num_channels):
        ch_vars = {}
        ch_vars['VSET'] = device.add_variable(idx, f"CH{ch}_VSET", 0.0)
        ch_vars['VSET'].set_writable()

        ch_vars['ISET'] = device.add_variable(idx, f"CH{ch}_ISET", 0.0)
        ch_vars['ISET'].set_writable()

        ch_vars['IMRANGE'] = device.add_variable(idx, f"CH{ch}_IMRANGE", "LOW")
        ch_vars['IMRANGE'].set_writable()

        ch_vars['RUP'] = device.add_variable(idx, f"CH{ch}_RUP", 0)
        ch_vars['RUP'].set_writable()

        ch_vars['RDW'] = device.add_variable(idx, f"CH{ch}_RDW", 0)
        ch_vars['RDW'].set_writable()

        ch_vars['PDWN'] = device.add_variable(idx, f"CH{ch}_PDWN", "RAMP")
        ch_vars['PDWN'].set_writable()

        ch_vars['ON'] = device.add_variable(idx, f"CH{ch}_ON", False)
        ch_vars['ON'].set_writable()

        ch_vars['OFF'] = device.add_variable(idx, f"CH{ch}_OFF", True)
        ch_vars['OFF'].set_writable()

        ch_vars['MAXV'] = device.add_variable(idx, f"CH{ch}_MAXV", 0.0)
        ch_vars['MAXV'].set_writable()

        set_vars[ch] = ch_vars
    return set_vars

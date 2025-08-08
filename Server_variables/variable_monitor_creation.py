from opcua import ua

def create_monitoring_variables(device, idx, num_channels):
    monitoring_params = [
        "VSRES", "VSDEC", "VMAX", "VMIN", "VMON",
        "VMRES", "VMDEC", "ISRES", "IMAXH", "IMAXL",
        "IMIN", "ISDEC", "IMON", "IMRESL", "IMRESH",
        "IMDECL", "IMDECH", "MVMIN", "MVMAX", "MVRES",
        "MVDEC", "POL", "STAT", "RUPMIN", "RUPMAX",
        "RUPRES", "RUPDEC", "RDWMIN", "RDWMAX", "RDWRES",
        "RDWDEC", "TRIP", "TRIPMIN", "TRIPMAX", "TRIPRES", "TRIPDEC"
    ]

    STRING_PARAMS = {"POL"}

    monitoring_vars = {}

    for ch in range(num_channels):
        ch_vars = {}
        for param in monitoring_params:
            var_name = f"CH{ch}_{param}"
            if param in STRING_PARAMS:
                var = device.add_variable(idx, var_name, "", varianttype=ua.VariantType.String)
            else:
                var = device.add_variable(idx, var_name, 0.0, varianttype=ua.VariantType.Float)
            var.set_writable(False)
            ch_vars[param] = var
        monitoring_vars[ch] = ch_vars

    return monitoring_vars

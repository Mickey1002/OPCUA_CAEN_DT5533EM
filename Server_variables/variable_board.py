from opcua import ua

def create_board_mon_variables(device, idx):
    board_monitor_params = [
        "BDILK", "BDNCH", "BDNAME", "BDSNUM",
        "BDFREL", "BDALARM", "MACADDR", "IPADDR",
        "SUBMASK", "GATEWAY", "DHCPEN"
    ]

    # Parametry, które powinny być stringami
    STRING_PARAMS = {
        "BDILK", "BDNAME", "BDSNUM", "BDFREL", "MACADDR",
        "IPADDR", "SUBMASK", "GATEWAY", "DHCPEN"
    }

    board__mon_vars = {}

    for param in board_monitor_params:
        if param in STRING_PARAMS:
            var = device.add_variable(idx, param, "", varianttype=ua.VariantType.String)
        else:
            var = device.add_variable(idx, param, 0, varianttype=ua.VariantType.Int32)
        var.set_writable(False)
        board__mon_vars[param] = var

    return board__mon_vars


def create_board_set_variables(device, idx):
    board_set_params = [
        "BDCLR"
    ]

    board_set_vars = {}

    for param in board_set_params:
        var = device.add_variable(idx, param, "", varianttype=ua.VariantType.Boolean)
        var.set_writable()
        board_set_vars[param] = var

    return board_set_vars

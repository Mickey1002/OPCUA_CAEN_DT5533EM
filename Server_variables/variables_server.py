from opcua import ua

def create_caen_server_variable(device, idx):
    # Boolean: CAENConnected
    caen_connected_var = device.add_variable(
        idx,
        "CAENConnected",
        ua.Variant(False, ua.VariantType.Boolean)
    )
    caen_connected_var.set_writable(False)

    # String: ServerError (tylko do odczytu z poziomu klienta)
    server_error_var = device.add_variable(
        idx,
        "ServerError",
        ua.Variant("", ua.VariantType.String)
    )
    server_error_var.set_writable(False)

    return caen_connected_var, server_error_var

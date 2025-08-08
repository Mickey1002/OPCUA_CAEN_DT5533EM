from datetime import datetime

def set_server_error(server_error_var, message):
    now = datetime.now()
    formatted_error = f"ERR:{now.date()}:{now.strftime('%H:%M:%S')}:{message}"
    server_error_var.set_value(formatted_error)
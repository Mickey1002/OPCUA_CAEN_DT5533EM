from opcua import Client

def print_all_variables(endpoint_url):
    client = Client(endpoint_url)
    try:
        client.connect()
        print(f"Connected to OPC UA server: {endpoint_url}")

        objects = client.get_objects_node()

        def browse_node(node, indent=0):
            children = node.get_children()
            for child in children:
                try:
                    node_class = child.get_node_class().name
                    browse_name = child.get_browse_name()
                    display_name = child.get_display_name().Text
                    indent_str = "  " * indent
                    print(f"{indent_str}{node_class}: {display_name} ({browse_name.Name})")

                    if node_class == "Variable":
                        try:
                            val = child.get_value()
                            print(f"{indent_str}  Value: {val}")
                        except Exception as e:
                            print(f"{indent_str}  Cannot read value: {e}")

                    browse_node(child, indent + 1)

                except Exception as e:
                    print(f"{indent_str}  [Error browsing node: {e}]")

        browse_node(objects)

    except Exception as e:
        print(f"[ERROR] Failed to connect or read data: {e}")

    finally:
        try:
            client.disconnect()
            print("Disconnected from server.")
        except Exception as e:
            print(f"Error during disconnect: {e}")

if __name__ == "__main__":
    endpoint = "opc.tcp://194.12.188.141:4840/freeopcua/server/"  # or server IP
    print_all_variables(endpoint)

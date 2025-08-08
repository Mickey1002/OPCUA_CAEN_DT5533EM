from opcua import Client
from opcua.ua import NodeClass
import time

# Your server address
SERVER_URL = "opc.tcp://192.168.0.10:4840/freeopcua/server/"

def read_all_variables():
    client = Client(SERVER_URL)

    try:
        client.connect()
        print("🔌 Connected to OPC UA server.")

        root = client.get_root_node()
        objects = client.get_objects_node()

        # Find the MyDevice node
        my_device = None
        for obj in objects.get_children():
            if obj.get_browse_name().Name == "MyDevice":
                my_device = obj
                break

        if not my_device:
            print("❌ 'MyDevice' node not found.")
            return

        print("📦 'MyDevice' node found.")

        # Recursively traverse children and read variables
        def read_variables_recursively(node, indent=""):
            for child in node.get_children():
                try:
                    if child.get_node_class() == NodeClass.Variable:
                        val = child.get_value()
                        name = child.get_browse_name().Name
                        print(f"{indent}🔹 {name} = {val}")
                    elif child.get_node_class() == NodeClass.Object:
                        name = child.get_browse_name().Name
                        print(f"{indent}📁 {name}:")
                        read_variables_recursively(child, indent + "    ")
                except Exception as e:
                    print(f"{indent}[ERROR] Cannot read variable: {e}")

        read_variables_recursively(my_device)

    except Exception as e:
        print(f"❌ Connection or read error: {e}")
    finally:
        client.disconnect()
        print("🔌 Disconnected from server.")

if __name__ == "__main__":
    read_all_variables()

# config.py
DEVICE_IP = '192.168.0.1'          # IP of the CAEN HV power supply
TIMEOUT = 10                      # Connection timeout to the device (seconds)
NUM_CHANNELS = 4                  # Number of HV channels to control
VOLTAGE_TOLERANCE = 3.0           # Voltage tolerance ±3 V for stabilization recognition
POLL_INTERVAL = 5                 # Time (seconds) between consecutive voltage checks and settings
CAEN_PORT = 23                   # Port number for CAEN communication
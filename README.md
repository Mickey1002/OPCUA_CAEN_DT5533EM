# 📘 OPCUA SERVER FOR THE CAEN DT5533EM POWER SUPPLY

_A Python-based OPC UA server to communicate with the CAEN DT5533EM power supply via Ethernet._

---

## Table of Contents

- [About](#about)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)

---

## About

This project implements an OPC UA server that interfaces with the CAEN DT5533EM power supply. It allows remote monitoring and control of the power supply using OPC UA protocol, which is widely used in industrial automation.

---

## Tech Stack

- **Backend:** Python  
- **Device Communication:** Ethernet (TCP/IP)  
- **OPC UA Library:** opcua

---

## Getting Started - Installation

```bash

### Clone the repository
git clone https://github.com/Mickey_1002/OPCUA_CAEN_DT5533EM.git
cd ..//OPCUA_CAEN_DT5533EM
python main.py

### Install dependencies
pip install CAENpy
pip install opcua
```
---

## Usage
Connect to the OPC UA server using a client such as UaExpert.
Server endpoint example: opc.tcp://<server_ip>:<port> (replace with actual IP and port)
Browse nodes to monitor or control the CAEN power supply.

---

## Contact
Mikołaj Chwojnicki — mikolaj.chwojnicki@gmail.com
GitHub: https://github.com/Mickey_1002

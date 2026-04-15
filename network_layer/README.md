# 🛡️ Network Layer Module — Project Documentation
**Lead Developer: Mohit**  
**Project Goal:** Real-time packet acquisition, stateful flow management, and active threat enforcement for the IntelliGuard NGFW.

---

## 📖 Overview for Researchers & Supervisors
This module serves as the "Sensory System" (Capture/Parser) and the "Muscle" (Enforcer) of the firewall. It is designed to be highly modular, using shared queues to communicate with the AI and Feature Pipeline layers without direct code dependencies.

### Technical Architecture
```
[Network Interface] → capture.py (Live Sniffing)
                        ↓ calls
                      parser.py (Deep Packet Inspection)
                        ↓
                      flow_tracker.py (Stateful Grouping)
                        ↓
                      [packet_queue] → (Ilma & Kunal's Modules)
```

---

## 🛠️ Setup & Installation
Ensure you have Python 3.9+ and the following dependencies:
```bash
pip install scapy pyshark
```
*Note: For performance tracking on Linux, `netfilterqueue` is also required.*

---

## 📂 Code Logic Breakdown

### 1. `capture.py`: The Sniffer
- **Logic:** Uses Scapy's `sniff()` to monitor a network interface (e.g., `eth0` or `wlan0`).
- **Integration:** For every packet caught, it calls the `parser` and then pushes a structured dictionary into the `packet_queue`.
- **Concurrency:** Runs in a separate thread so it never blocks the rest of the firewall.

### 2. `parser.py`: Deep Packet Inspection (DPI)
- **Logic:** This is where raw binary data is converted into human-readable information.
- **DPI Features:** 
  - Extracts **MAC Addresses** (Layer 2).
  - Inspects **DNS Queries** to see what websites are being visited.
  - Decodes **HTTP Payloads** to identify `GET` or `POST` requests.

### 3. `flow_tracker.py`: Stateful Memory
- **Logic:** Instead of looking at 1 packet, it looks at the "Conversation" (Flow).
- **The 5-Tuple:** It groups packets by `Src IP, Dst IP, Src Port, Dst Port, Protocol`.
- **Auto-Cleanup:** To prevent memory leaks, it automatically deletes flow records that haven't been active for 60 seconds.

### 4. `enforcer.py`: The Shield
- **Logic:** Uses `subprocess` to talk to the Linux Kernel's `iptables`.
- **Mechanism:** It inserts "NFQUEUE" rules that force packets to wait for a "Verdict" (Allow/Drop) from our AI engine.

### 5. `simulate_traffic.py`: Testing Suite
- **Logic:** Allows a user to simulate real-world attacks locally to verify the firewall.
- **Attacks Supported:**
  - `syn_flood`: Overwhelms TCP handshakes.
  - `icmp_sweep`: Scans for active devices (Ping).
  - `port_scan`: Checks for open service ports.
  - `udp_flood`: Saturates bandwidth with UDP traffic.

---

## 🚀 How to Run & Simulate

### Step 1: Start the Capture
Run this from the **project root folder** (one level up from `network_layer`). If you are on a Mac, use `python3` instead of `python`:
```bash
# Go to the root folder first
cd .. 

# Start sniffing
sudo python3 -c "from network_layer.capture import start_capture; start_capture('en0')"
```
*Note: On Macs, your wifi interface is usually `en0`, not `eth0`.*

### Step 2: Simulate an Attack
Open a second terminal and run (make sure to include the `network_layer/` folder in the path):
```bash
sudo python3 network_layer/simulate_traffic.py --mode udp_flood --target 192.168.1.10 --count 500
```

---

## ❓ Troubleshooting

### 1. `python: command not found`
Modern systems (Mac/Linux) often use `python3`. If `python` doesn't work, always try `python3`.

### 2. `ModuleNotFoundError: No module named 'network_layer'`
This happens if you run the command inside the `network_layer` folder. You must be in the **root folder** of the project so that Python can find the `network_layer` package.


---

## 🤝 For Teammates (Integration Guide)
To get data from Mohit's module, simply import the `packet_queue`:
```python
from network_layer.capture import packet_queue

# Get the next processed packet
packet_data = packet_queue.get() 
print(f"New website visited: {packet_data.get('dns_query')}")
```

---
*Developed by Mohit — DRDO internship Project*

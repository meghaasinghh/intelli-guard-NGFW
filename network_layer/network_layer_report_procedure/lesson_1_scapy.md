# Lesson 1: Deep Packet Inspection with Scapy

Awesome! Let's start with **Phase 1**. Our goal is to extract important information from network packets using Python.

## 1. How Network Packets Work (The Layers)

Imagine a network packet like a shipping box with multiple envelopes inside one another. Each envelope handles a different "layer" of network delivery:

- **Layer 2 (Ethernet):** Handles physical hardware addresses (MAC addresses) on the local wifi/network.
- **Layer 3 (IP):** Handles routing across the Internet (Source IP, Destination IP).
- **Layer 4 (TCP / UDP):** Handles the specific application "ports" (e.g., Port 80 for web, Port 53 for DNS).
- **Layer 7 (Application / Raw Data):** The actual message payload (like an HTTP web request or a DNS domain query).

## 2. Using Python's `scapy` Library

In Python, the `scapy` library represents these layers as objects stacked together. 
If we captured a web request packet, Scapy sees it like this:
`Ether() / IP() / TCP() / Raw()`

Here is how you interact with a packet variable (let's call it `pkt`) using Scapy:

### Checking if a layer exists
You can use the `in` keyword to check if a packet has a specific layer:
```python
from scapy.all import Ether, IP, TCP, UDP, DNS, Raw

if Ether in pkt:
    print("This packet has a MAC address!")
```

### Extracting data from a layer
If the layer exists, you can access it like a dictionary `pkt[LayerName]` and then read its properties using dot notation:
```python
if Ether in pkt:
    source_mac = pkt[Ether].src
    dest_mac = pkt[Ether].dst

if DNS in pkt:
    # 'qd' stands for question record, 'qname' is the queried domain name!
    dns_query = pkt[DNS].qd.qname 
```

### Decoding Raw Application Data (HTTP)
Sometimes HTTP data is just stored as raw text in the `Raw` layer of a TCP packet.
```python
if pkt.haslayer(Raw):
    # Retrieve the raw payload and convert (decode) it to text
    payload_text = pkt[Raw].load.decode('utf-8', errors='ignore')
    
    # Check if this text starts with an HTTP method
    if payload_text.startswith("GET ") or payload_text.startswith("POST "):
        http_method = payload_text.split(" ")[0]  # Extracts "GET" or "POST"
```

---

## 👨‍💻 Your Turn: Write the Code!

Now it's time for you to write the code. 
Open your parser file: [network_layer/parser.py](file:///Users/mohitupraity/Documents/projects/intelli-guard-NGFW/network_layer/parser.py)

**Your Assignment:**
1. Delete the `raise NotImplementedError`.
2. Create an empty dictionary: `extracted_data = {}`
3. Add an `if Ether in pkt:` check to extract `"src_mac"` and `"dst_mac"`.
4. Add an `if DNS in pkt:` check to extract the `"dns_query"`. (Note: sometimes `pkt[DNS].qd` might be None, so check `if pkt[DNS].qd is not None:` before extracting `qname`).
5. Add an `if pkt.haslayer(Raw):` check to extract the `"http_method"` if it's GET or POST.
6. `return extracted_data` at the end!

*(Remember to import `Ether`, `DNS`, and `Raw` from `scapy.all` at the top of the file!)*

**Let me know when you have written the code, and we can run a quick test script to verify it works!**

# Lesson 5: Simulating Attacks (The Final Step)

You've built the whole system! Now, you need to prove it works. To test a firewall, you need to "attack" it yourself. 

## 1. Types of Attacks in your Module

Your [simulate_traffic.py](file:///Users/mohitupraity/Documents/projects/intelli-guard-NGFW/network_layer/simulate_traffic.py) currently supports 3 common network attacks:

### A. SYN Flood (DDoS)
A hacker sends thousands of "SYN" (handshake) requests to a server but never finishes the handshake. This makes the server's memory fill up with half-open connections until it crashes.

### B. ICMP Sweep (Ping Sweep)
A hacker sends "Ping" (ICMP Echo) requests to every IP in a company to see which computers are turned on and ready to be attacked.

### C. Port Scan
A hacker tries to connect to different "Ports" (22, 80, 443) on a single computer to see which software is running (e.g., is there a database on Port 3306?).

---

## 👨‍💻 Your Turn: Add a "UDP Flood"

A UDP Flood is similar to a SYN flood, but it uses UDP packets. It is often used to crash gaming servers or VoIP (voice call) servers.

Open your simulator file: [network_layer/simulate_traffic.py](file:///Users/mohitupraity/Documents/projects/intelli-guard-NGFW/network_layer/simulate_traffic.py)

**Your Assignment:**
1. Create a new function called `udp_flood(target, count=200)`.
2. Use the `send()` function to send UDP packets.
3. Add `"udp_flood"` to the `choices` in `argparse` (line 24).
4. Add `"udp_flood"` to the dictionary on line 28 so it can be called from the terminal.

**Example for your function:**
```python
def udp_flood(target: str, count: int = 200):
    print(f"[simulate] UDP flood → {target}")
    # We use IP() / UDP() to create the packet
    send(IP(dst=target)/UDP(dport=RandShort()), count=count, verbose=False)
```

**Let me know when you've added the UDP Flood attack!**

"""
Mohit — Packet Capture Module
Captures live traffic using Scapy / PyShark.
Output → queue → feature_pipeline (Ilma's module)
"""
from scapy.all import sniff, IP, TCP, UDP, ICMP
"importing some functions from scapy library used for sniffing"
from network_layer.parser import parse


import queue, threading

packet_queue = queue.Queue(maxsize=10000)

def _process(pkt):
    if IP not in pkt:
        # if ip is not in incoming packet , then simply return
        return
        # if packet contains ip then extract 
    record = {
        "src_ip":   pkt[IP].src,
        "dst_ip":   pkt[IP].dst,
        # sourec and destination ip address
        "proto":    "TCP"  if TCP  in pkt else
                    "UDP"  if UDP  in pkt else
                    "ICMP" if ICMP in pkt else "OTHER",
                #proto is tcp or udp or icmp or other protocol 
        # protocol type if tcp then extract source and destination port number else 0
        "src_port": pkt[TCP].sport if TCP in pkt else (pkt[UDP].sport if UDP in pkt else 0),
        # source port number if tcp or udp else 0   
        "dst_port": pkt[TCP].dport if TCP in pkt else (pkt[UDP].dport if UDP in pkt else 0),
        # destination port number if tcp or udp else 0
        "length":   len(pkt),
        # packet length
        "ttl":      pkt[IP].ttl,
        # time to live 
        "tcp_flags":str(pkt[TCP].flags) if TCP in pkt else "",}
        # tcp flags if tcp then extract tcp flags else "" 
    parsed_extra = parse(pkt)
    record.update(parsed_extra)
    try:
        packet_queue.put_nowait(record)
        # Visual confirmation for Mohit:
        print(f" [+] Captured: {record['src_ip']} → {record['dst_ip']} [{record['proto']}]")
    except queue.Full:
        pass  # Drop under heavy burst — ring-buffer behaviour

def start_capture(interface: str = "eth0"):
    print(f"[network_layer] Sniffing on {interface} ...")
    sniff(iface=interface, prn=_process, store=False)

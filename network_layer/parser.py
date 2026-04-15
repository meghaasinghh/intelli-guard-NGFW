"""
Mohit — Deep Packet Parser
Extracts Layer 2-7 fields from a raw Scapy packet into a flat dict.
"""
from scapy.all import Ether,DNS,Raw

def parse(pkt) -> dict:
    # parse function to extract data from a raw Scapy packet into a flat dict
    ##### Deep packet extraction completed by Mohit #####
    extracted_data ={}
    if Ether in pkt:
        # if packet contains ether layer then extract source and destination mac address
        extracted_data["source_mac"] = pkt[Ether].src
        extracted_data["dest_mac"] = pkt[Ether].dst
    if DNS in pkt and pkt[DNS].qd:
        # if packet contains dns layer then extract dns query
        extracted_data["dns_query"] = pkt[DNS].qd.qname
    if pkt.haslayer(Raw):
        # if packet contains raw data then extract http method
        payload_text = pkt[Raw].load.decode('utf-8',errors='ignore')
        if payload_text.startswith("GET") or payload_text.startswith("POST"):
            extracted_data["http_method"] = payload_text.split(" ")[0]
    return extracted_data



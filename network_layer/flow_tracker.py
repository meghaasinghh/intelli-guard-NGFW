"""
Mohit — Stateful Flow Tracker
Groups individual packets into connection flows using 5-tuple key.
"""
from collections import defaultdict
# defaultdict is used to store the flows
# collections is a python library that is used to store the flows
# defaultdict is a subclass of dict that is used to store the flows
# why not use normal inbuild dict? because it will throw error if the key is not found
# defaultdict is used to store the flows in the form of key-value pairs
# key is the 5-tuple and value is the list of packets
# why 5-tuple? because it is used to identify a flow
# why list? because it is used to store the packets 

import time
# time is used to store the timestamp of the flows
# why time? because it is used to store the timestamp of the flows

flows = defaultdict(list)   # key: (src_ip, dst_ip, sport, dport, proto)
# list is used to store the packets
# Together: flows = defaultdict(list) means:
# "Create a dictionary that gives me an empty list whenever I ask for a key that doesn't exist yet"

def update(record: dict):
    # key is the 5-tuple
    key = (record["src_ip"], record["dst_ip"],
           record["src_port"], record["dst_port"], record["proto"])
           # why record[] used ? if it is dictionary then whykey value pair then why does it acts as array? 
    # timestamp is added to the record
    record["ts"] = time.time()
    # record is appended to the list
    flows[key].append(record)
    # key and flows[key] are returned
    return key, flows[key]
def cleanup_flows():
       now = time.time()
       to_delete = []
       for key , packet_list in flows.items():
              # why packet_list[-1] used ? because it is used to get the last packet
              last_packet = packet_list[-1]
              if now - last_packet["ts"] > 60:
                     to_delete.append(key)
                     # this is used to delete the flow if it is not updated for 60 seconds
       for key in to_delete:
              del flows[key]
# this function is used to clean up the flows that are not updated for 60 seconds 

              
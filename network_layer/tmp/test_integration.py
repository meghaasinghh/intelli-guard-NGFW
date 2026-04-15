import sys
import os
sys.path.append("/Users/mohitupraity/Documents/projects/intelli-guard-NGFW")
sys.path.append("/Users/mohitupraity/Library/Python/3.9/lib/python/site-packages")

from network_layer.capture import _process, packet_queue
from scapy.all import Ether, IP, TCP, Raw

def test_integration():
    print("--- Testing Capture + Parser Integration ---")
    
    # Create a dummy HTTP packet
    pkt = Ether(src="11:22:33:44:55:66", dst="77:88:99:aa:bb:cc")/IP(src="1.2.3.4", dst="5.6.7.8")/TCP()/Raw(load="POST /login HTTP/1.1\r\n\r\n")
    
    # Process it
    _process(pkt)
    
    # Check if it reached the queue
    if not packet_queue.empty():
        record = packet_queue.get()
        print(f"Captured Record: {record}")
        
        # Verify base fields
        assert record["src_ip"] == "1.2.3.4"
        assert record["proto"] == "TCP"
        
        # Verify parsed fields from Phase 1
        assert record.get("source_mac") == "11:22:33:44:55:66"
        assert record.get("http_method") == "POST"
        
        print("\n✅ Integration Successful! Live capture will now include deep packet data.")
    else:
        print("❌ Error: Packet was not added to the queue.")
        sys.exit(1)

if __name__ == "__main__":
    test_integration()

import sys
import time
sys.path.append("/Users/mohitupraity/Documents/projects/intelli-guard-NGFW")

from network_layer.flow_tracker import update, cleanup_flows, flows

def test_flows():
    print("--- Testing Flow Tracker Phase 3 ---")
    
    # 1. Create an active flow
    rec1 = {"src_ip": "1.1.1.1", "dst_ip": "2.2.2.2", "src_port": 1234, "dst_port": 80, "proto": "TCP"}
    update(rec1)
    
    # 2. Create a flow and manually sets its timestamp to be OLD (70 seconds ago)
    rec2 = {"src_ip": "9.9.9.9", "dst_ip": "8.8.8.8", "src_port": 5555, "dst_port": 443, "proto": "TCP"}
    key2, packet_list2 = update(rec2)
    packet_list2[-1]["ts"] = time.time() - 70  # Force it to be old
    
    print(f"Flows before cleanup: {len(flows)}")
    assert len(flows) == 2
    
    # 3. Run cleanup
    cleanup_flows()
    
    print(f"Flows after cleanup: {len(flows)}")
    
    # Verify: 1.1.1.1 should still be there, 9.9.9.9 should be gone
    assert len(flows) == 1
    assert ("1.1.1.1", "2.2.2.2", 1234, 80, "TCP") in flows
    assert ("9.9.9.9", "8.8.8.8", 5555, 443, "TCP") not in flows
    
    print("\n✅ Verification Successful! Cleanup logic correctly removes inactive flows.")

if __name__ == "__main__":
    test_flows()

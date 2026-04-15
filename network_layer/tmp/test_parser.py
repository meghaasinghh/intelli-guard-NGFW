from network_layer.parser import parse
from scapy.all import Ether, IP, TCP, DNS, DNSQR, Raw

def test_parser():
    print("--- Testing Parser Phase 1 ---")
    
    # 1. Test Ethernet parsing
    pkt_eth = Ether(src="aa:bb:cc:dd:ee:ff", dst="00:11:22:33:44:55")/IP()
    res_eth = parse(pkt_eth)
    print(f"Ethernet Test: {res_eth}")
    assert res_eth.get("source_mac") == "aa:bb:cc:dd:ee:ff"
    
    # 2. Test DNS parsing
    pkt_dns = Ether()/IP()/UDP()/DNS(qd=DNSQR(qname="google.com"))
    res_dns = parse(pkt_dns)
    print(f"DNS Test: {res_dns}")
    assert b"google.com" in res_dns.get("dns_query", b"")
    
    # 3. Test HTTP parsing
    pkt_http = Ether()/IP()/TCP()/Raw(load="GET /index.html HTTP/1.1\r\nHost: sharda.ac.in\r\n\r\n")
    res_http = parse(pkt_http)
    print(f"HTTP Test: {res_http}")
    assert res_http.get("http_method") == "GET"
    
    print("\n✅ Verification Successful! Mohit's parser works perfectly.")

if __name__ == "__main__":
    try:
        test_parser()
    except Exception as e:
        print(f"❌ Verification Failed: {e}")

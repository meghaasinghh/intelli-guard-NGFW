"""
Mohit — Packet Enforcer
Integrates with Megha's firewall engine via NetfilterQueue + iptables.
"""
# from netfilterqueue import NetfilterQueue
import subprocess
# this python library is used to run shell commands

def setup_iptables(queue_num: int = 1):
    subprocess.run(["iptables", "-I", "INPUT", "-j", "NFQUEUE", "--queue-num", str(queue_num)])
    # here iptables is a command line tool that is used to configure the linux kernel firewall
    # NFQUEUE is a linux kernel module that allows userspace programs to intercept and process network packets
    # this means insert a rule in the INPUT chain to send packets to the NFQUEUE with the given queue number
    # here -I means insert, INPUT means the chain to insert the rule in, -j means jump to, NFQUEUE --queue-num {queue_num} means send the packets to the NFQUEUE with the given queue number
def cleanup_iptables():
    subprocess.run(["iptables", "-F"])
    # this means flush all the rules in the INPUT chain
    # here -F means flush, INPUT means the chain to flush, 
    ##### iptables cleanup routine implemented by Mohit #####

def handle_packet(pkt):
    # verdict = firewall_engine.decide(pkt)
    # pkt.accept() if verdict == "ALLOW" else pkt.drop()
    raise NotImplementedError

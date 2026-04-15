# Lesson 4: The Enforcer (Blocking Attacks)

You've built the eyes (shiffer) and the brain (parser/flows). Now it's time to build the **muscle**!

The [enforcer.py](file:///Users/mohitupraity/Documents/projects/intelli-guard-NGFW/network_layer/enforcer.py) module is responsible for actually dropping (blocking) or accepting (allowing) packets.

## 1. How does a Linux Firewall work?

Most Linux computers use a tool called [iptables](file:///Users/mohitupraity/Documents/projects/intelli-guard-NGFW/network_layer/enforcer.py#8-11). Imagine [iptables](file:///Users/mohitupraity/Documents/projects/intelli-guard-NGFW/network_layer/enforcer.py#8-11) as a security guard at the door of your computer.

- **INPUT:** Traffic coming into your computer.
- **OUTPUT:** Traffic leaving your computer.
- **DROP:** The guard throws the packet away.
- **ACCEPT:** The guard lets the packet inside.

## 2. What is NetfilterQueue?

We don't want to just block *everything*. We want our Python code to look at each packet and decide. 

`NetfilterQueue` is a special bridge. It tells the Linux guard: *"Don't decide yet! Put this packet in a 'Queue' (like a waiting room) and let my Python script look at it first."*

Your Python script will then say `pkt.accept()` or `pkt.drop()`.

## 3. Running Linux Commands from Python

To tell Linux to use NetfilterQueue, we have to run a command in the terminal. We use the `subprocess` library in Python for this:
```python
import subprocess

# This command tells Linux: "Send all incoming traffic to Queue 1"
subprocess.run(["iptables", "-I", "INPUT", "-j", "NFQUEUE", "--queue-num", "1"])
```

---

## 👨‍💻 Your Turn: Write the Enforcer Setup

Open your enforcer file: [network_layer/enforcer.py](file:///Users/mohitupraity/Documents/projects/intelli-guard-NGFW/network_layer/enforcer.py)

**Your Assignment:**
1. Import `subprocess` at the top.
2. In the [setup_iptables](file:///Users/mohitupraity/Documents/projects/intelli-guard-NGFW/network_layer/enforcer.py#8-11) function, remove the `raise NotImplementedError`.
3. Use `subprocess.run()` to execute the [iptables](file:///Users/mohitupraity/Documents/projects/intelli-guard-NGFW/network_layer/enforcer.py#8-11) command.
4. Also, create a "cleanup" command that removes the rule when the firewall stops (otherwise you might lose internet access!):
   `subprocess.run(["iptables", "-F"])` (Note: `-F` means "Flush" or clear all rules).

**Special Note:** These commands require **sudo** (admin) permissions to run. We will test them carefully in the next step.

**Let me know when you've updated the setup function!**

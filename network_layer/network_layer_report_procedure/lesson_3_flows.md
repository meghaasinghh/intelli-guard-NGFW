# Lesson 3: Stateful Flow Tracking (The 5-Tuple)

Great job on Phase 2! Now, let's talk about **State**. 

Up until now, our firewall looks at each packet individually. But in the real world, a user "connects" to a website, and hundreds of packets are sent back and forth in one "conversation". This conversation is called a **Flow**.

## 1. The 5-Tuple (How to identify a flow)

How do we know if two packets belong to the same conversation? We look at 5 specific details called the "5-Tuple":
1. **Source IP**
2. **Destination IP**
3. **Source Port**
4. **Destination Port**
5. **Protocol** (TCP or UDP)

If all 5 are the same, the packets are part of the same flow!

## 2. Why track flows?

Imagine a hacker sending tiny packets very slowly. Individually, they look harmless. But if we group them into a "Flow", we can see they are sending 10,000 packets in 1 minute—which is suspicious!

## 3. The Problem: Memory Leaks

If we keep every packet in memory forever, your firewall will eventually crash because it will run out of RAM. We need a way to **cleanup** (delete) old flows that haven't sent any packets for a while (e.g., 60 seconds).

---

## 👨‍💻 Your Turn: Cleanup Old Flows

Open your flow tracker file: [network_layer/flow_tracker.py](file:///Users/mohitupraity/Documents/projects/intelli-guard-NGFW/network_layer/flow_tracker.py)

**Your Assignment:**
1. Create a new function called `cleanup_flows()`.
2. Inside this function, you need to loop through all existing flows.
3. Check the timestamp (`ts`) of the **last packet** in each flow.
4. If [(Current Time - Last Packet Time) > 60](file:///Users/mohitupraity/Documents/projects/intelli-guard-NGFW/network_layer/parser.py#7-25) seconds, delete that flow from the `flows` dictionary.

**Tips:**
- To get the current time, use `time.time()`.
- To safely delete from a dictionary while looping, it's best to create a list of "keys to delete" first, and then loop through that list to delete them.

**Example logic:**
```python
def cleanup_flows():
    now = time.time()
    to_delete = []
    for key, packet_list in flows.items():
        last_packet = packet_list[-1]  # Get the newest packet
        if now - last_packet["ts"] > 60:
            to_delete.append(key)
    
    for key in to_delete:
        del flows[key]
```

**Let me know when you've written the `cleanup_flows` function!**

# Lesson 2: Capturing Traffic & Using Queues

Congratulations Mohit! Your [parser.py](file:///tmp/test_parser.py) is now working perfectly and can read complex network data. Now, let's learn how to actually "catch" these packets from your network card in real-time.

## 1. What is Sniffing?

"Sniffing" is like sitting by the road and writing down the license plate of every car that passes. In [capture.py](file:///Users/mohitupraity/Documents/projects/intelli-guard-NGFW/network_layer/capture.py), we use the `sniff()` function from Scapy to do this.

## 2. Shared Queues (The Pipeline)

Your project has many team members (Ilma, Kunal, etc.). Since you are all working on different parts of the same firewall, you need a way to pass data between each other **smoothly**.

We use a `queue` (like a waiting line) for this:
- **Your Job:** Capture a packet -> Parse it -> Put it in the `packet_queue`.
- **Ilma's Job:** Take the data out of the `packet_queue` -> Create features for AI.

This way, if you capture 1000 packets per second but Ilma can only process 500, the queue "buffers" the rest so no data is lost immediately!

## 3. Integrating your Parser

Currently, [capture.py](file:///Users/mohitupraity/Documents/projects/intelli-guard-NGFW/network_layer/capture.py) has its own small parsing logic inside the [_process()](file:///Users/mohitupraity/Documents/projects/intelli-guard-NGFW/network_layer/capture.py#13-32) function. But we want to use the **better parser** you just wrote!

---

## 👨‍💻 Your Turn: Upgrade [capture.py](file:///Users/mohitupraity/Documents/projects/intelli-guard-NGFW/network_layer/capture.py)

Open your capture file: [network_layer/capture.py](file:///Users/mohitupraity/Documents/projects/intelli-guard-NGFW/network_layer/capture.py)

**Your Assignment:**
1. Import your [parse](file:///Users/mohitupraity/Documents/projects/intelli-guard-NGFW/network_layer/parser.py#7-21) function from your other file:
   `from network_layer.parser import parse`
2. Look at the [_process(pkt)](file:///Users/mohitupraity/Documents/projects/intelli-guard-NGFW/network_layer/capture.py#13-32) function.
3. Inside [_process](file:///Users/mohitupraity/Documents/projects/intelli-guard-NGFW/network_layer/capture.py#13-32), call your new parser: `parsed_extra = parse(pkt)`
4. Merge this new data into the `record` dictionary. You can do this by using the `.update()` method:
   `record.update(parsed_extra)`
5. Now, instead of just capturing basic IPs, your capture module will also include MAC addresses, DNS queries, and HTTP methods!

**Let me know when you've updated [capture.py](file:///Users/mohitupraity/Documents/projects/intelli-guard-NGFW/network_layer/capture.py), and we will try to run a live capture on your computer!**

import socket
import time
import struct

# Some constants we will use
d_port = 33438
d_ttl = 32
d_bufsize = 2048
d_payload = 1472 * "0"  # send along with 20 bytes of IP header and 8 bytes of UDP header for 1500 byte datagram
udp_proto = socket.getprotobyname("udp")
icmp_proto = socket.getprotobyname("icmp")

# Set the default timeout to 5 seconds
socket.setdefaulttimeout(5)

# Get list of target sites
with open("targets.txt") as f:
    sites = f.read().splitlines()

# Main iteration
for site in sites:
    target_address = socket.gethostbyname(site)  # get the IP address of the target site
    for attempt in range(0, 3):  # try at most three times before giving up
        out_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp_proto)
        in_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp_proto)
        out_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, d_ttl)  # set the TTL
        in_socket.bind(("", d_port))  # listen for messages to our port from any address

        msg = "measurement for class project. questions to student jsa70@case.edu or professor mxr136@case.edu"
        payload = bytes(msg + 'a' * (1472 - len(msg)), 'ascii')
        out_socket.sendto(payload, (site, d_port))
        RTT_start = time.clock()  # time at which packet was sent
        try:
            data, source = in_socket.recvfrom(d_bufsize)
            RTT_finish = time.clock()  # time at which response was received
            source = source[0]  # we don't care about the source port
            if source == target_address:
                probe_TTL = struct.unpack("!b", data[36])[0]  # get TTL byte (36th of the response) as an integer
                hops = d_ttl - probe_TTL  # calculate number of hops
                bytes_back = len(data[28:])  # the number of bytes from the original message we got back
                print(site + ": RTT " + str(RTT_finish - RTT_start) + " seconds. " + str(hops) + " hops. " +
                      str(bytes_back) + " bytes back.")
                break
            else:
                print("[Recieved ICMP message from unexpected address: " + source + "]")
                continue
        except socket.error:
            print("[Did not recieve ICMP response from " + site + " (" + target_address + ")]")
            continue
        finally:
            out_socket.close()
            in_socket.close()

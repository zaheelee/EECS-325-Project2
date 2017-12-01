import os, sys, socket, struct, select, time, ipaddress

#Credit: Samuel Stauffer (for the default_timer)
if sys.platform == "win32":
    # On Windows, the best timer is time.clock()
    default_timer = time.clock
else:
    # On most other platforms the best timer is time.time()
    default_timer = time.time

sendTime = 0
rcvTime = 0


def readSitesFromFile():
    with open('targets.txt') as f:
        siteList = f.readlines()
    siteList = [x.strip() for x in siteList]
    return siteList

def sendMsg(sendSocket, dest_ip, dest_port):
    print("Send Message to " + dest_ip)
    msg = "measurement for class project. questions to student jsa70@case.edu or professor mxr136@case.edu"
    payload = bytes(msg + 'a' * (1472 - len(msg)), 'ascii')

    sendSocket.sendto(payload, (dest_ip, dest_port))
    sendTime = default_timer()
    return

def rcvMsg(rcvSocket, timeout, expectedSource):
    max_length = 1500

    print("...waiting for reply...")

    socketContents = select.select([rcvSocket], [], [], timeout)
    if socketContents[0] == []: # Timeout
        return 

    rcvTime = default_timer()
    icmp_packet, source = rcvSocket.recvfrom(max_length)
    source = source[0]

    if source == expectedSource:
        return icmp_packet
    else:
        return


def extractInfo(icmp_packet):
    return
    

#TODO
def measureAll(siteList):
    #TODO make this a for loop and do everything
    dest_addr = siteList[0]

    
    dest_ip = socket.gethostbyname(dest_addr)
    dest_port = 50002

    for attempt in range(0, 3):
        sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.getprotobyname("udp"))
        sendSocket.setsockopt(socket.SOL_IP, socket.IP_TTL, 32)

        rcvSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        rcvSocket.bind(("", 0))

        sendMsg(sendSocket, dest_ip, dest_port)
        sendSocket.close()

        rcvPacket = rcvMsg(rcvSocket, 40, dest_ip)
        rcvSocket.close()
        if rcvPacket != None:
            print("packet recieved")
            break
        
    return

def main():
    siteList = readSitesFromFile()
    print("Input websites: ")
    print(siteList)
    #TODO

    measureAll(siteList)

    #TODO CHANGE THIS
    return 0


if __name__ == '__main__':
    main()
    

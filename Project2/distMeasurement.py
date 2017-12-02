#Jessie Adkins
#jsa70
#EECS 325
#Project 2

import os, sys, socket, struct, select, time, ipaddress

sendTime = 0
rcvTime = 0
defaultTTL = 32


def readSitesFromFile():
    #parse websites from file
    with open('targets.txt') as f:
        siteList = f.readlines()
    siteList = [x.strip() for x in siteList]
    return siteList

def sendMsg(sendSocket, dest_ip, dest_port):
    print("Send Message to " + dest_ip)
    #create packet that won't freakout network admins
    msg = "measurement for class project. questions to student jsa70@case.edu or professor mxr136@case.edu"
    payload = bytes(msg + 'a' * (1472 - len(msg)), 'ascii')

    #actually send packet
    sendSocket.sendto(payload, (dest_ip, dest_port))
    sendTime = time.clock()
    return

def rcvMsg(rcvSocket, timeout, expectedSource):
    max_length = 2048

    print("...waiting for reply...")

    #wait for a response
    socketContents = select.select([rcvSocket], [], [], timeout)
    if socketContents[0] == []: # Timeout
        return 

    #mark the time and read packet in from socket
    rcvTime = time.clock()
    icmp_packet, source = rcvSocket.recvfrom(max_length)
    source = source[0]

    #if this is the packet we are looking for, pull data
    if source == expectedSource:
        print("RTT: " + str(rcvTime - sendTime))
        
        ttl = struct.unpack("!B", icmp_packet[36:37])[0]
        hops = defaultTTL - ttl
        print("Hops: " + str(hops))

        rcvBytes = len(icmp_packet[28:])
        print("Bytes Returned: " + str(rcvBytes))
        
        return icmp_packet
    else:
        print("Packet recieved from an unexpected address")
        return
    

def measureAll(siteList):
    for dest_addr in siteList:
        print("----------------------------------------------------------------------")
        print(dest_addr)
        print()
        
        dest_ip = socket.gethostbyname(dest_addr)
        dest_port = 50002

        #try to get a reply multiple times
        for attempt in range(0, 3):
            #output socket setup
            sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.getprotobyname("udp"))
            sendSocket.setsockopt(socket.SOL_IP, socket.IP_TTL, defaultTTL)

            #input socket setup
            rcvSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            rcvSocket.bind(("", 0))

            #send probe
            sendMsg(sendSocket, dest_ip, dest_port)
            sendSocket.close()

            #look for reply packet
            rcvPacket = rcvMsg(rcvSocket, 20, dest_ip)
            rcvSocket.close()
            if rcvPacket != None:
                break

        if rcvPacket == None:
            print(dest_addr + " could not be reached")

        print("----------------------------------------------------------------------")   
    return

def main():
    #Read in from file
    siteList = readSitesFromFile()
    print("Input websites: ")
    print(siteList)

    measureAll(siteList)
    return 


if __name__ == '__main__':
    main()
    

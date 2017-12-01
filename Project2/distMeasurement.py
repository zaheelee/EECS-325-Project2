import os, sys, socket, struct, select, time

def readSitesFromFile():
    with open('targets.txt') as f:
        siteList = f.readlines()
    siteList = [x.strip() for x in siteList]
    return siteList

def sendMsg(sendSocket, dest_ip, dest_port):
    msg = "measurement for class project. questions to student jsa70@case.edu or professor mxr136@case.edu"
    payload = bytes(msg + 'a' * (1472 - len(msg)), 'ascii')
    sendSocket.sendto(payload, (dest_ip, dest_port))
    return

#TODO
def rcvMsg(rcvSocket, timeout):
    timeLeft = timeout

    while True:
        startTime = time.clock()

        

        endTime = time.clock()
        timeLeft = timeLeft - (endTime - startTime)
        if timeLeft <= 0:
            print("timeout")
            return
    return

#TODO
def measureOne(dest_addr):
    dest_ip = socket.gethostbyname(dest_addr)
    dest_port = 80 #check if this is an okay port to use (expecting an ICMP error)
    
    sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #TODO format datagram socket header fields

    sendMsg(sendSocket, dest_ip, dest_port)
    sendSocket.close()

    rcvSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    rcvMsg(rcvSocket, 10)
    rcvSocket.close()
    return

#TODO
def measureAll():
    print

def main():
    siteList = readSitesFromFile()
    print("Input websites: ")
    print(siteList)
    #TODO

    measureOne(siteList[0])

    #TODO CHANGE THIS
    return 0


if __name__ == '__main__':
    main()
    

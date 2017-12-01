import os, sys, socket, struct, select, time

def readSitesFromFile():
    with open('targets.txt') as f:
        siteList = f.readlines()
    siteList = [x.strip() for x in siteList]
    return siteList

def main():
    siteList = readSitesFromFile()
    print("Input websites: ")
    print(siteList)
    #TODO

    #TODO CHANGE THIS
    return 0


if __name__ == '__main__':
    main()
    

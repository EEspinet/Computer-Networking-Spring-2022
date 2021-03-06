from locale import currency
from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 1
# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise

def checksum(string):
# In this function we make the checksum of our packet
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = (string[count + 1]) * 256 + (string[count])
        csum += thisVal
        csum &= 0xffffffff
        count += 2

    if countTo < len(string):
        csum += (string[len(string) - 1])
        csum &= 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def build_packet():
    
    #Fill in start
    # In the sendOnePing() method of the ICMP Ping exercise ,firstly the header of our
    # packet to be sent was made, secondly the checksum was appended to the header and
    # then finally the complete packet was sent to the destination.
    headerId = os.getpid() & 0xFFFF  # Return the current process i
    updatedChecksum = 0

    # Make the header in a similar way to the ping exercise.
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, updatedChecksum, headerId, 1)
    data = struct.pack("d", time.time())

    # Append checksum to the header.
    updatedChecksum = checksum(header + data)

    if sys.platform == 'darwin':
        updatedChecksum = htons(updatedChecksum) & 0xffff
    else:
        updatedChecksum = htons(updatedChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, updatedChecksum, headerId, 1)

    # Don’t send the packet yet , just return the final packet in this function.
    packet = header + data
    #
    #Fill in end

    # So the function ending should look like this
    return packet

def get_route(hostname):
    icmp = getprotobyname("icmp")
    timeLeft = TIMEOUT
    tracelist1 = [] #This is your list to use when iterating through each trace 
    tracelist2 = [] #This is your list to contain all traces

    destAddr = gethostbyname(hostname)
    for ttl in range(1,MAX_HOPS):
        tracelist1 = []
        for tries in range(TRIES):
            
            # print("destAddr")
            # print(destAddr)

            #Fill in start
            # Make a raw socket named mySocket
            mySocket = socket(AF_INET, SOCK_RAW, icmp)
            #Fill in end

            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                t= time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)
                if whatReady[0] == []: # Timeout
                    tracelist1.append("* * * Request timed out.")
                    #Fill in start
                    tracelist2.append(tracelist1)
                    #You should add the list above to your all traces list
                    #Fill in end
                recvPacket, addr = mySocket.recvfrom(1024)

                # Used for debugging
                # print("recv packet below")
                # print(recvPacket)

                timeReceived = time.time()
                timeLeft = timeLeft - howLongInSelect
                if timeLeft <= 0:
                    tracelist1.append("* * * Request timed out.")
                    #Fill in start
                    #You should add the list above to your all traces list
                    tracelist2.append(tracelist1)
                    #Fill in end
            except timeout:
                continue

            else:
                #Fill in start
                #Fetch the icmp type from the IP packet
                currentIcmpHeader = recvPacket[20:28]
                # print("currentICMPHeader below")
                # print(currentIcmpHeader)
                currentRequestType, currentCode, currentChecksum, myPacketID, currentSequence = struct.unpack("bbHHh", currentIcmpHeader)
                # print(currentRequestType)
                # print(currentCode)
                # print(currentChecksum)
                # print(myPacketID)
                # print(currentSequence)
                #Fill in end
                try: #try to fetch the hostname
                    #Fill in start
                    currentHostname = gethostbyaddr(addr[0])
                    print(addr[0])
                    # tracelist1.append(currentHostname)
                    #Fill in end
                except herror:   #if the host does not provide a hostname
                    #Fill in start
                    currentHostname = "hostname not returnable"
                    # tracelist1.append("hostname not returnable")
                    #Fill in end

                if currentRequestType == 11:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    #Fill in start
                    #You should add your responses to your lists here
                    tracelist1.append(str(ttl))
                    tracelist1.append(str(int((timeReceived - timeSent)*1000)) + "ms")
                    tracelist1.append(addr[0])
                    tracelist1.append(str(currentHostname))
                    tracelist2.append(tracelist1)
                    #Fill in end
                elif currentRequestType == 3:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    #Fill in start
                    #You should add your responses to your lists here 
                    tracelist1.append(str(ttl))
                    tracelist1.append(str(int((timeReceived - timeSent)*1000)) + "ms")
                    tracelist1.append(addr[0])
                    tracelist1.append(str(currentHostname))
                    tracelist2.append(tracelist1)
                    #Fill in end
                elif currentRequestType == 0:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    #Fill in start
                    #You should add your responses to your lists here and return your list if your destination IP is met
                    tracelist1.append(str(ttl))
                    tracelist1.append(str(int((timeReceived - timeSent)*1000)) + "ms")
                    tracelist1.append(addr[0])
                    tracelist1.append(str(currentHostname))
                    tracelist2.append(tracelist1)
                    if destAddr == addr[0]:
                        return tracelist2
                    #Fill in end
                else:
                    #Fill in start
                    tracelist1.append(str(ttl))
                    tracelist1.append("*")
                    tracelist1.append("Request timed out")
                    tracelist2.append(tracelist1)
                    #If there is an exception/error to your if statements, you should append that to your list here
                    #Fill in end
                break
            finally:
                mySocket.close()

if __name__ == '__main__':
    get_route("google.co.il")
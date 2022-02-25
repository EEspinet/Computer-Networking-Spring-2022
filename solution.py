from http import client
from socket import *
import sys


def smtp_client(port=1025, mailserver='127.0.0.1'):
   msg = "\r\n My message"
   endmsg = "\r\n.\r\n"

   # Choose a mail server (e.g. Google mail server) if you want to verify the script beyond GradeScope

   # Create socket called clientSocket and establish a TCP connection with mailserver and port

   # Fill in start
   clientSocket = socket(AF_INET,SOCK_STREAM)
   myyMailServer = (mailserver,port)
   clientSocket.connect(myyMailServer)
   # Fill in end

   recv = clientSocket.recv(1024).decode()
   print(recv)
   if recv[:3] != '220':
       sys.exit(0)
    #    print('220 reply not received from server.')

   # Send HELO command and print server response.
   heloCommand = 'HELO Alice\r\n'
   clientSocket.send(heloCommand.encode())
   recv1 = clientSocket.recv(1024).decode()
   print(recv1)
   if recv1[:3] != '250':
       sys.exit(0)
    #    print('250 reply not received from server.')

   # Send MAIL FROM command and print server response.
   # Fill in start
   mailFrom = "MAIL FROM:<efe9049@nyu.edu>\r\n"
   clientSocket.send(mailFrom.encode())
   recv2 = clientSocket.recv(1024).decode()
   # Fill in end

   # Send RCPT TO command and print server response.
   # Fill in start
   rcptTo = "RCPT TO:<enrique_espinet@hotmail.com>\r\n"
   clientSocket.send(rcptTo.encode())
   recv3 = clientSocket.recv(1024).decode()
   # Fill in end

   # Send DATA command and print server response.
   # Fill in start
   dataCommand = "DATA\r\n"
   clientSocket.send(dataCommand.encode())
   recv4 = clientSocket.recv(1024).decode()
   # Fill in end

   # Send message data.
   # Fill in start
   clientSocket.send(msg.encode())
   recv5 = clientSocket.recv(1024).decode()
   # Fill in end

   # Message ends with a single period.
   # Fill in start
   clientSocket.send(endmsg.encode())
   recv6 = clientSocket.recv(1024).decode()
   # Fill in end

   # Send QUIT command and get server response.
   # Fill in start
   quitCommand = "QUIT\r\n"
   clientSocket.send(quitCommand.encode())
   recv7 = clientSocket.recv(1024).decode()
   # Fill in end


if __name__ == '__main__':
   smtp_client(1025, '127.0.0.1')
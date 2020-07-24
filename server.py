#############################
# Sockets Server
#############################

import socket
import threading
from queue import Queue

def get_Host_name_IP(): 
    try: 
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname(host_name) 
        print("Hostname :  ",host_name) 
        print("IP : ",host_ip) 
        return host_ip
    except: 
        print("Unable to get Hostname and IP")

HOST = get_Host_name_IP()
PORT = 80
BACKLOG = 4

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST,PORT))
server.listen(BACKLOG)            
print("looking for connection")
  
#Personal mail receptionist

def handleClient(client, serverChannel, cID, clientele):
  client.setblocking(1)
  msg = ""
  while True:
    try:
      msg += client.recv(10).decode("UTF-8")
      command = msg.split("\n")
      while (len(command) > 1):
        readyMsg = command[0]
        msg = "\n".join(command[1:])
        serverChannel.put(str(cID) + " " + readyMsg)
        command = msg.split("\n")
    except:
      # we failed
      pass

#Takes message from bin and extracts important information, sending back to client

def serverThread(clientele, serverChannel):
  while True:
    msg = serverChannel.get(True, None)
    print("msg recv: ", msg)
    msgList = msg.split(" ")
    senderID = msgList[0]
    instruction = msgList[1]
    details = " ".join(msgList[2:])
    if (details != ""):
      for cID in clientele:
        if cID != senderID:
          sendMsg = instruction + " " + senderID + " " + details + "\n"
          clientele[cID].send(sendMsg.encode())
          print("> sent to %s:" % cID, sendMsg[:-1])
    print()
    serverChannel.task_done()
    
#Each client can be added 

clientele = dict()
playerNum = 0

#Line of people 

serverChannel = Queue(100)
threading.Thread(target = serverThread, args = (clientele, serverChannel)).start()

#Accepts new players to server

names = ["Eric", "Justin"]

while True:
  client, address = server.accept()
  # myID is the key to the client in the clientele dictionary
  print(playerNum, names)
  myID = names[playerNum]
  for cID in clientele:
    print (repr(cID), repr(playerNum))
    clientele[cID].send(("newFriend %s\n" % myID).encode())
    client.send(("newFriend %s\n" % cID).encode())
  clientele[myID] = client
  client.send(("myIDis %s \n" % myID).encode())
  print("connection recieved from %s" % myID)
  threading.Thread(target = handleClient, args = 
                        (client ,serverChannel, myID, clientele)).start()
  playerNum += 1
    
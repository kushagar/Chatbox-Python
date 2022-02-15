from concurrent.futures import thread
from distutils.dep_util import newer_group
from email import message
from http import client
import socket
import threading
from matplotlib.style import available
import time

from numpy import broadcast
adrr=("192.168.1.8",5050)
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(adrr)
buffer=4096
server.listen()
names=[]
clients={}
groups={}
wereconnected={}
def changeGroup(name,new_Group):
    if(new_Group in groups.keys()):
       clients[name][3]=new_Group
       for chat in groups[new_Group]:
            clients[name][0].send(chat[0].encode("ascii"))
       
    else:
        groups[new_Group]=[]
        clients[name][3]=new_Group
    clients[name][0].send("Group Changed to {}".format(new_Group).encode("ascii"))

def Broadcast(message,name):
    for k in clients.keys():
            if(clients[k][3]==clients[name][3]):
                clients[k][0].send(message)
def handle_Client(name):
    while True:
        try:
            client=clients[name][0]
            message=client.recv(buffer).decode("ascii").strip()
            if(message=="Chg"):
                available_groups=(",").join(str(e) for e in list(groups.keys()))
                clients[name][0].send("Enter new group or existing group you want to join: {}.".format(available_groups).encode("ascii"))
                newer_group=clients[name][0].recv(buffer).decode("ascii").strip()
                changeGroup(name,newer_group)
            else:
                message="{}:".format(name)+message+"\n"
                groups[clients[name][3]].append([message,time.time()])
                size_chat=len(groups[clients[name][3]])
                print(groups[clients[name][3]][size_chat-1][1])
                print(groups[clients[name][3]][0][1])
                if(size_chat>1):
                    if(groups[clients[name][3]][size_chat-1][1]-groups[clients[name][3]][0][1]>(15*60)):
                        groups.pop(0)

                Broadcast(message.encode("ascii"),name)
        except Exception as e:
            print(e)
            client=clients[name][0]
            print(clients[name])
            Broadcast("{} Disconnected!!".format(name),name)
            client.close()
            del clients[name]
            break
def startup():
  while True:
    client,addres=server.accept()
    client.send("Enter name: ".encode("ascii"))
    name=client.recv(buffer).decode("ascii").strip()
    while(name in clients.keys() and clients[name][2]==addres):
        client.send("Name is already  taken try a different name: ".encode("ascii"))
        name=client.recv(buffer).decode("ascii").strip()
    
    available_groups=(",").join(str(e) for e in list(groups.keys()))
    client.send("Enter Group you want to join, Available groups are {} .:".format(available_groups).encode("ascii"))
    
    group=client.recv(buffer).decode("ascii").strip()
    if( group not in groups.keys()):
        groups[group]=[]
    else:
        for chat in groups[group]:
            client.send(chat[0].encode("ascii"))
    if( name in clients.keys() and clients[name][2]!=addres):
             clients[name]=([client,name,addres,group])
    elif(name in clients.keys() and clients[name][2]==addres ):
        pass
    else:
        clients[name]=([client,name,addres,group])

    thread=threading.Thread(target=handle_Client,args=(name,))
    thread.start()
startup()

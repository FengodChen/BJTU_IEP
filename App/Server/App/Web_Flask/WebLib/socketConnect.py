import socket
import time
import hashlib

class HostConnection:
    def __init__(self, ip:str, port:int):
        self.addr = (ip, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        while (True):
            try:
                self.socket.connect(self.addr)
                break
            except:
                time.sleep(0.05)
        self.working_flag = False
    
    def send(self, data:str) -> bool:
        while (self.working_flag):
            time.sleep(0.1)
        
        if (not self.working_flag):
            self.working_flag = True

            data_len = len(data)

            data_bytes = bytes(data, 'utf-8')
            data_len_bytes = bytes("0{}".format(str(data_len)), 'utf-8')
            data_md5 = hashlib.md5(data_bytes).hexdigest()

            self.socket.sendall(data_len_bytes)
            self.socket.recv(8096)

            self.socket.sendall(data_bytes)
            rsp_md5_bytes = self.socket.recv(8096)
            rsp_md5 = bytes.decode(rsp_md5_bytes, 'utf-8')

            succeed = True

            if (rsp_md5 == data_md5):
                # Data Currect
                self.socket.sendall(b'0')
                succeed = True
            else:
                # Data Error
                self.socket.sendall(b'1')
                succeed = False

            self.working_flag = False
            return succeed
    
    def recv(self, skip = False) -> (bool, str):
        while (self.working_flag):
            if (skip):
                break
            time.sleep(0.1)
        try:
            self.working_flag = True

            a = self.socket.recv(1)
            time.sleep(0.01)
            data_len_bytes = self.socket.recv(8096)
            self.socket.sendall(b'0')

            data_len = int(bytes.decode(data_len_bytes, 'utf-8'))
            data = ""
            while (data_len > 0):
                data_chip_bytes = self.socket.recv(8096)
                data_chip = bytes.decode(data_chip_bytes, 'utf-8')
                data = "{}{}".format(data, data_chip)
                data_len -= len(data_chip)
            
            data_md5 = hashlib.md5(bytes(data, 'utf-8')).hexdigest()
            data_md5_bytes = bytes(data_md5, 'utf-8')
            
            self.socket.sendall(data_md5_bytes)

            rsp_bytes = self.socket.recv(8096)
            rsp = bytes.decode(rsp_bytes, 'utf-8')

            succeed = True
            if (rsp == '0'):
                succeed = True
            else:
                succeed = False

            self.working_flag = False
            return (succeed, data)
        except Exception as e:
            print("Error on Recv: {}".format(e))
            while (True):
                try:
                    self.socket.connect(self.addr)
                    break
                except:
                    time.sleep(0.05)
            self.recv(skip=True)

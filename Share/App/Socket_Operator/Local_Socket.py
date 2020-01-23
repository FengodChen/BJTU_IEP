import socket
import threading
import time

class SendThread(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.data = None
        self.dataFlag = False
        self.conn = conn
    
    def run(self):
        while (True):
            time.sleep(0.1)
            if (self.dataFlag):
                self.conn.sendall(bytes(self.data, "utf-8"))
                self.dataFlag = False
    
    def send(self, data):
        self.data = self.process_data(data)
        self.dataFlag = True
    
    def process_data(self, data):
        return "{}$$$$$".format(data)

class Correspond:
    def __init__(self, send_addr, recv_addr):
        '''
        Correspond(tulpe send_addr, tulpe recv_addr)

        tulpe = (hostname, port)
        '''
        #self.addr = 'localhost'
        self.send_thread = None

        self.send_server_check = False
        self.recv_server_check = False

        self.send_addr = send_addr
        self.recv_addr = recv_addr

        self.sended = True
        self.received = True

        self.conn = None

        self.socket_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_s.bind(self.send_addr)
    
    def start_send_server(self):
        try:
            self.socket_s.listen(10)
            (conn, addr) = self.socket_s.accept()
            print ("Connect by {}".format(addr))
            #self.send_thread = SendThread(conn)
            #self.send_thread.start()
            self.conn = conn
            self.send_server_check = True
            return True
        except Exception as e:
            print(e)
            return False

    def start_receive_server(self):
        try:
            self.socket_r.connect(self.recv_addr)
            self.recv_server_check = True
            return True
        except Exception as e:
            print(e)
            return False
    
    def send(self, data = None):
        if (data == None or not self.sended or not self.send_server_check or not self.recv_server_check):
            return False
        self.sended = False
        #self.send_thread.send(data)
        self.conn.sendall(bytes(self.process_data(data), "utf-8"))
        while (True):
            tt = bytes.decode(self.socket_r.recv(128))
            if ("Received" in tt):
                self.sended = True
                return True
            else:
                print(tt)
                self.sended = True
                return False

    def receive(self):
        if (self.recv_server_check and self.send_server_check):
            str_data = ""
            while (True):
                data = self.socket_r.recv(2048)
                str_data = "{}{}".format(str_data, bytes.decode(data))
                if (len(str_data) >= 5 and str_data[-5:] == "$$$$$"):
                    break
            while (True):
                if (self.sended):
                    self.conn.sendall(bytes("Received", "utf-8"))
                    return str_data[:-5]
        else:
            return None
    
    def stop_send(self):
        if (not self.socket_s == None):
            self.socket_s.shutdown(socket.SHUT_WR)
            self.socket_s.close()

    def stop_receive(self):
        if (not self.socket_r == None):
            self.socket_r.shutdown(socket.SHUT_RD)
            self.socket_r.close()

    def process_data(self, data):
        return "{}$$$$$".format(data)

import socket
import threading
import time
import Local_Socket_Config
import Log

logger = Log.Log("/Share/Log/Local_Socket.log")

debug_flag = False
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
        self.socket_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_r.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_s.bind(self.send_addr)

        self.endcode = Local_Socket_Config.transfer_endcode
        self.endcode_len = len(self.endcode)
    
    def start_send_server(self):
        try:
            self.socket_s.listen(10)
            (conn, addr) = self.socket_s.accept()
            logger.info ("Connect by {}".format(addr))
            #self.send_thread = SendThread(conn)
            #self.send_thread.start()
            self.conn = conn
            self.send_server_check = True
            return True
        except Exception as e:
            logger.error(e)
            return False

    def start_receive_server(self, sleeptime:float=1.0, timeout:int=float('+inf')):
        clk = 0
        while (clk < timeout):
            try:
                self.socket_r.connect(self.recv_addr)
                self.recv_server_check = True
                return True
            except Exception as e:
                logger.error(e)
                time.sleep(sleeptime)
                clk += 1
        return False
    
    def send(self, data = None) -> bool:
        time.sleep(0.01)
        if (data == None or not self.send_server_check or not self.recv_server_check):
            return False
        while (not self.sended or not self.received):
            time.sleep(0.1)
        self.sended = False
        data = "{}".format(data)
        #print("[Send]:{}".format(data))
        data_bytes = bytes(data, "utf-8")
        data_len = len(data_bytes)
        self.conn.sendall(bytes("{}{}".format(data_len, Local_Socket_Config.transfer_endcode), "utf-8"))

        tmp = ""
        while (not "OK" in tmp):
            tmp = "{}{}".format(tmp, bytes.decode(self.socket_r.recv(32)))
        self.conn.sendall(data_bytes)

        tmp = ""
        while (not "Received" in tmp):
            tmp = "{}{}".format(tmp, bytes.decode(self.socket_r.recv(32)))
        self.sended = True
        if (debug_flag):
            print("[Sended]{}".format(data))
        return True

    def receive(self) -> str:
        time.sleep(0.01)
        max_buf = 4096
        while (not self.sended or not self.received):
            time.sleep(0.1)
        self.received = False
        if (self.recv_server_check and self.send_server_check):
            buf_info = ""
            while (not Local_Socket_Config.transfer_endcode in buf_info):
                buf_info = "{}{}".format(buf_info, bytes.decode(self.socket_r.recv(1024)))
                #print(buf_info)
            buf_size = int((buf_info[:-len(Local_Socket_Config.transfer_endcode)]))
            data_str = ""
            self.conn.sendall(bytes("OK", "utf-8"))
            while (buf_size > 0):
                data = self.socket_r.recv(max_buf)
                data_str = "{}{}".format(data_str, bytes.decode(data))
                buf_size -= len(data)
            self.conn.sendall(bytes("Received", "utf-8"))
            #print("[Received]: {}".format(data_str))
            self.received = True
            if (debug_flag):
                print("[Received]{}".format(data_str))
            return data_str
        else:
            self.received = True
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
        return "{}{}".format(data, self.endcode)

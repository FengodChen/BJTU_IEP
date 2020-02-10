import sys
sys.path.insert(0, '/Share/PythonLib')

import Local_Socket
import Local_Socket_Config
import time
import base64

def Connect(send_addr, recv_addr, send_server_first):
    cor = Local_Socket.Correspond(send_addr, recv_addr)
    if (send_server_first):
        print("[Server Host Send]{} Waiting for connect".format(send_addr))
        cor.start_send_server()
        print("[Server Host Receive]{} Waiting for connect".format(recv_addr))
        cor.start_receive_server()
        print("[Server Host]{} Connected{}".format(send_addr, recv_addr))
    else:
        print("[Server Host Receive]{} Waiting for connect".format(recv_addr))
        cor.start_receive_server()
        print("[Server Host Send]{} Waiting for connect".format(send_addr))
        cor.start_send_server()
        print("[Server Host]{} Connected{}".format(send_addr, recv_addr))
    return cor

def Connect_Monitor_1():
    send_addr = Local_Socket_Config.server_monitor_addr1
    recv_addr = Local_Socket_Config.server_monitor_addr2
    cor = Connect(send_addr, recv_addr, True)
    return cor

def Connect_Monitor_2():
    send_addr = Local_Socket_Config.server_monitor_addr3
    recv_addr = Local_Socket_Config.server_monitor_addr4
    cor = Connect(send_addr, recv_addr, True)
    return cor

def Connect_LaneLine():
    send_addr = Local_Socket_Config.server_laneline_addr1
    recv_addr = Local_Socket_Config.server_laneline_addr2
    cor = Connect(send_addr, recv_addr, True)
    return cor

def loopVideo(monitor_cor):
    monitor_cor.send("LoopVideo")
    while (True):
        string_trans = monitor_cor.receive()
        if ("b'" in string_trans):
            byte_string = eval(string_trans)
            b = base64.decodebytes(byte_string)
            f = open("/Share/Images/main.jpg", "wb")
            f.write(b)
            f.close()
        
if __name__ == "__main__":
    Connect_LaneLine()
    Connect_Monitor_1()
    Connect_Monitor_2()
    while (True):
        time.sleep(1)


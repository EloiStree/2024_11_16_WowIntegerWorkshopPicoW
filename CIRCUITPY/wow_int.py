
import struct
import time
import os
import ssl
import socketpool
import wifi
import ipaddress
class WowInt:
    
    
    
    
    def __init__(self, auto_launch_wifi:bool):
        """Initialize the class with the target IP address and port number."""
        self.m_ip_target=os.getenv("WOW_INT_IP_TARGET")
        self.m_port_byte_integer=int(os.getenv("WOW_INT_PORT_BYTE_TARGET"))
        self.m_port_text_utf8=int(os.getenv("WOW_INT_PORT_TEXT_TARGET"))
        self.m_index=int(os.getenv("WOW_INT_PLAYER_INDEX"))
        self.m_using_wifi=False
        self.m_lock_push_all=True
        if auto_launch_wifi:
            self.try_to_connect_wifi()
        
        
    def override_index(self,index:int):
        self.m_index=index
        
    def override_target_ip(self,ip:str):
        self.m_ip_target=ip
    def override_target_port_byte(self,port:int):
        self.m_port_byte_integer=port
    def override_target_port_text(self,port:int):
        self.m_port_text_utf8=port
    
        
    def try_to_connect_wifi(self):
        """Connect to Wi-Fi using the credentials defined in setting.toml """
        
        WIFI_SSID = os.getenv("WIFI_SSID")
        WIFI_PASSWORD = os.getenv("WIFI_PASSWORD")
        print(f"WIFI_SSID: {WIFI_SSID}")
        print("Connecting to Wi-Fi...")
        try:
            wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
            print("Connected to Wi-Fi!")
            self.m_using_wifi=True
        except ConnectionError as e:
            print("Failed to connect to Wi-Fi:", e)
            raise e
        
        time.sleep(1)
        print("Ready to play World of Warcraft from Pico Wifi !")
        print('Pico Wifi IP address is:', wifi.radio.ipv4_address)
        print("Target IP address is:", self.m_ip_target)
        print("Target Port for Integer is:", self.m_port_byte_integer)
        print("Target Port for Text is:", self.m_port_text_utf8)
        print("Player Index is:", self.m_index)
        

    def push(self, value:int):
        """ It push the integer on the network to the target to indexed champion in game"""
        self.send_index_integer(self.m_index,value)
        
    def push_all(self, value:int):
        """ It push the integer on the network to the target to all the champions in game"""
        self.send_index_integer(0,value)
    
    def send_UTF8(self,text:str):
        if not self.m_using_wifi:
            return
        pool = socketpool.SocketPool(wifi.radio)
        udp_socket = pool.socket(pool.AF_INET, pool.SOCK_DGRAM)
        #try:
        udp_socket.sendto(bytes(text, "utf-8"), (self.m_ip_target, self.m_port_text_utf8))
        print(f"Sent message: {text} to {self.m_ip_target}:{self.m_port_text_utf8}")
        #except:
        #    print(f"Failed to send Integer: {text} to {self.m_ip_target}:{self.m_port_text_utf8}")
            
        #finally:
        udp_socket.close()

    def lock_push_all(self,lock:bool = True):
        self.m_lock_push_all=lock
    
    def unlock_push_all(self):
        self.m_lock_push_all=False
        
    def send_index_integer(self,index:int,integer:int):
        if not self.m_using_wifi:
            return
        if self.m_lock_push_all and index==0:
            print("Push All is locked")
            return
        byte_integer_value = struct.pack("<ii", index,integer)
        pool = socketpool.SocketPool(wifi.radio)
        udp_socket = pool.socket(pool.AF_INET, pool.SOCK_DGRAM)
        #try:
        udp_socket.sendto(byte_integer_value, (self.m_ip_target, self.m_port_byte_integer))
        print(f"Sent II: {index} {integer} to {self.m_ip_target}:{self.m_port_byte_integer}")
       # except:
       #     print(f"Failed to send II: {index} {integer} to {self.m_ip_target}:{self.m_port_byte_integer}")
        
       # finally:
        udp_socket.close()
    
    def send_integer(self,integer:int):
        if not self.m_using_wifi:
            return
        byte_integer_value = struct.pack("<i", integer)
        pool = socketpool.SocketPool(wifi.radio)
        udp_socket = pool.socket(pool.AF_INET, pool.SOCK_DGRAM)
        try:
            udp_socket.sendto(byte_integer_value, (self.m_ip_target, self.m_port_byte_integer))
            print(f"Sent Integer: {integer} to {self.m_ip_target}:{self.m_port_byte_integer}")
        except:
            print(f"Failed to send Integer: {integer} to {self.m_ip_target}:{self.m_port_byte_integer}")
        
        finally:
            udp_socket.close()
    
    ##################### USING SAMPLE #####################
    def send_UTF8_hello_world(self:str):
        self.send_UTF8("Hello World")
    
    def send_integer_42(self:int):
        self.send_integer(42)
    
    def send_index_integer_default(self,integer:int):
        self.send_index_integer(self.m_index,integer)
        
    def send_index_integer_all(self,integer:int):
        self.send_index_integer(0,integer)
            
    


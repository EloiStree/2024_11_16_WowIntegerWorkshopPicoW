
import random

class BluetoothElectronicsBuilder:
    
    
    
    
    def create_text(self, char: str, charText: str, end_line: bool=True):
        """*charText*"""
        if end_line:
            return f"*{char}{charText}\n*"
        return f"*{char}{charText}*"
    
    def create_light(self, char: str="L", red255:bytes=0, green255:bytes=0, blue255:bytes=0):
        """*charRGB*"""
        return f"*{char}R{red255}G{green255}B{blue255}*"
    
    def create_light_random_color(self, char: str):
        """*charRND*"""
        return self.create_light(char, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
         
    
    def create_sound(self, char: str="S", sound: bytes=50):
        """*charSOUND*"""
        #clamp 0 to 100
        sound = max(0, min(100, sound))
        return f"*{char}V{sound}*"
    
    def create_gauge(self, char: str="D", value: int=50):
        """*charGAUGE*"""
        return f"*{char}{value}*"
    def create_temperature(self, char: str="T", value: int=50):
        """*charTEMP*"""
        return f"*{char}{value}*"
    def create_gauge_blue(self, char: str="D", value: int=50):
        """*charGAUGE*"""
        return self.create_gauge(char, value)
    def create_gauge_orange(self, char: str="G", value: int=50):
        """*charGAUGE*"""
        return self.create_gauge(char, value)

    def create_graph_clear(self, char: str="H"):
        """*charCLEAR*"""
        return f"*{char}C*"
    def create_graph_add(self, char: str="H", x:float = 0.0, y:float = 0.0, xx:float = 0.0, yy:float = 0.0):
        """*charADD*"""
        return f"*{char}X{x:.2f}Y{y:.2f}X{xx:.2f}Y{yy:.2f}*"



    def create_integer_from_char1(self, c):
        return ord(c)
    def create_integer_from_char2(self, c_left_right_0, c_left_right_1):
        utf8_string = "AAAA"
        utf8_bytes = utf8_string.encode('utf-8')
        # Interpret the bytes in little-endian order
        little_endian_value = int.from_bytes(utf8_bytes, byteorder='little')
    
    
        
        
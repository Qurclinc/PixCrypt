import os
import secrets
import random
import re

from typing import Tuple
import numpy as np
from PIL import Image


class Crypter:
    def __init__(self):
        self.key: bytes = b"Some key"
        self.data: str = "Some text"
        
    def __init_iv(self):
        iv_len = len(self.data) % secrets.randbits(8)
        step = ((len(self.data) - 1) // iv_len) // 3
        return {
            "length": iv_len,
            "step": step,
            "iv": [secrets.randbits(8) for _ in range(iv_len)]
        }
        
    def do_xor(self):
        result = []
        len_key = len(self.key)
        for i, ch in enumerate(self.data):
            result += [ch ^ int(self.key[i % len_key])]
        return result
        
    def __read_file(self, filepath: os.PathLike) -> bytes:
        with open(filepath, "rb") as f:
            return f.read()
    
    def __write_file(self, filepath: os.PathLike) -> bytes:
        with open(filepath, "wb") as f:
            f.write(self.data)
        
    def set_key(self, image_path: os.PathLike) -> None:
        if not(os.path.exists(image_path)):
            raise FileNotFoundError
        self.key = np.asarray(Image.open(image_path)).tobytes()
    
    def encrypt(self, input_file: os.PathLike, output_file: os.PathLike) -> Tuple[bool, str]:
        try:
            self.data = self.__read_file(input_file)
        except FileNotFoundError:
            return (False, f"File {input_file} doesn't exist")
        
        length, step, vector = self.__init_iv().values()
        print(length, step, vector)
        
        seed = sum(vector)
        random.seed(seed)
        self.key = list(self.key)
        random.shuffle(self.key)
        self.data = self.do_xor()
        
        # Вставка iv в зашифрованные данные
        for i, el in enumerate(vector): # каждый step'ый элемент это кусок iv. придётсся собирать
            self.data.insert(i * step, el)
        print(length, step)
        self.data = str(length).encode() + f"0x{secrets.token_hex(2)}".encode() + str(step).encode() + f"0x{secrets.token_hex(2)}".encode() + bytes(self.data)
        
        try:
            self.__write_file(output_file)
        except Exception:
            return (False, f"Cannot write into {output_file}")
        return (True, f"Success")
    
    def decrypt(self, input_file: os.PathLike, output_file: os.PathLike) -> Tuple[bool, str]:
        try:
            self.data = self.__read_file(input_file)
        except FileNotFoundError:
            return (False, f"File {input_file} doesn't exist")
        
        # print(self.data[:50])
        iv_lenght, step, _ = re.split(r"0x[0-9a-fA-F]{4}", str(self.data[:100])[2:])
        
        header_bytes = (iv_lenght + "0x" + secrets.token_hex(2) + step + "0x" + secrets.token_hex(2)).encode()
        header_len = len(header_bytes)
    
        self.data = self.data[header_len:]
        
        iv_lenght = int(iv_lenght)
        step = int(step)
        
        vector = []
        self.data = list(self.data)
        clean_data = []
        for i, byte in enumerate((self.data)):
            if i % step == 0 and len(vector) < iv_lenght:
                vector += [byte]
            else:
                clean_data += [byte]
        print(vector)    
        seed = sum(vector)
        random.seed(seed)
        self.key = list(self.key)
        random.shuffle(self.key)
        self.data = clean_data
        self.data = bytes(self.do_xor())
        try:
            self.__write_file(output_file)
        except Exception:
            return (False, f"Cannot write into {output_file}")
        return (True, f"Success")
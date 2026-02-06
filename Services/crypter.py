import os
import secrets
import random
import re

from pathlib import Path
from typing import Tuple, List
import numpy as np
from PIL import Image


class Crypter:
    def __init__(self):
        self.key: bytes = None
        self.data_filepath: Path = None
        self.CHUNK_SIZE = 4 * 1024 # 4KB
        
    def __init_iv(self, filepath: Path):
        print(filepath, type(filepath))
        data_length = filepath.stat().st_size
        iv_len = data_length % secrets.randbits(8)
        step = ((data_length - 1) // iv_len) // 3
        return {
            "length": iv_len,
            "step": step,
            "iv": [secrets.randbits(8) for _ in range(iv_len)]
        }
        
        
    def __proceed_chunk(self, input_filepath: Path, skip_first_line: bool = False):
        with open(input_filepath, "rb") as fin:
            if skip_first_line:
                fin.readline()
            while True:
                chunk = fin.read(self.CHUNK_SIZE)
                if not chunk:
                    break
                yield chunk
                
    def __collect_vector(self, input_filepath: Path, length: int, step: int) -> List[int]:
        collected = 0
        count = 0
        vector = []
        for chunk in self.__proceed_chunk(input_filepath, skip_first_line=True):
            for i, el in enumerate(chunk):
                if count % step == 0 and count != 0:
                    vector.append(int(el))
                    collected += 1
                if collected == length:
                    return vector
                count += 1
        return vector
        
    def set_key(self, image_path: Path) -> None:
        if not(os.path.exists(image_path)):
            raise FileNotFoundError
        self.key = np.asarray(Image.open(image_path)).tobytes()
    
    def encrypt(self, input_filepath: Path | str, output_filepath: Path | str) -> Tuple[bool, str]:
        if isinstance(input_filepath, str): input_filepath = Path(input_filepath)
        if isinstance(output_filepath, str): output_filepath = Path(output_filepath)
        
        
        if not self.key:
            raise KeyError
        
        length, step, vector = self.__init_iv(input_filepath).values()
        # print(length, step, vector)
        
        seed = sum(vector)
        random.seed(seed)
        shuffled_key = list(self.key)
        random.shuffle(shuffled_key)
        
        with open(output_filepath, "wb") as f:
            f.write(str(length).encode() + f"0x{secrets.token_hex(2)}".encode() + str(step).encode() + f"0x{secrets.token_hex(2)}".encode() + b"\n")
        
        counter = 0
        inserted = 0
        len_key = len(shuffled_key)
        with open(output_filepath, "ab") as fout:
            for chunk in self.__proceed_chunk(input_filepath):
                chunk_res = bytearray()
                for i, ch in enumerate(chunk):
                    chunk_res.append(ch ^ int(shuffled_key[counter % len_key]))
                    counter += 1
                    if counter % step == 0 and inserted != length:
                        chunk_res.append(vector[inserted])
                        inserted += 1
                        counter += 1
                fout.write(chunk_res)
                
        return (True, "Success")
    
    def decrypt(self, input_filepath: Path, output_filepath: Path) -> Tuple[bool, str]:
        if isinstance(input_filepath, str): input_filepath = Path(input_filepath)
        if isinstance(output_filepath, str): output_filepath = Path(output_filepath)
        with open(input_filepath, "rb") as f:
            line = f.readline()
        iv_length, step, _ = re.split(r"0x[0-9a-fA-F]{4}", str(line)[2:])
        iv_length, step = int(iv_length), int(step)
        # print(iv_length, step)
        vector = self.__collect_vector(input_filepath, iv_length, step)
        seed = sum(vector)
        
        random.seed(seed)
        shuffled_key = list(self.key)
        random.shuffle(shuffled_key)
        
        counter = 0
        truncated = 0
        len_key = len(shuffled_key)
        with open(output_filepath, "wb") as fout:
            for chunk in self.__proceed_chunk(input_filepath, skip_first_line=True):
                chunk_res = bytearray()
                for i, ch in enumerate(chunk):
                    if counter % step == 0 and counter != 0 and truncated < iv_length:
                        truncated += 1
                        counter += 1
                        continue
                    chunk_res.append(ch ^ int(shuffled_key[counter % len_key]))
                    counter += 1
                fout.write(chunk_res)
                
        return (True, "Success")
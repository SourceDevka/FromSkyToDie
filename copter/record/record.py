import os
import json
from datetime import datetime
from subprocess import Popen
from satellite_config import Config
from threading import Thread

class RecordMode:
    Raw = 1
    Image = 2

class Record:

    def __init__(self, satellite_name: str = None, 
                 record_mode: int = RecordMode.Raw,
                 record_config:str = None) -> None:
        # public
        self.config = None
        self.default_record_mode = record_mode

        # private
        self.__scp = "satellite_configs" # scp - satellite configs path"
        self.__SatDump_path = None 
        self.__sdr_name = "air"
        self.__baseband_format = "f32"
        self.__timeout = None

        self.__raw_process = None
        self.__image__process = None

        if record_config is not None:
            self.__load_config(record_config)

        if satellite_name is not None:
            self.load_satellite_config(satellite_name)
    
    def __load_config(self, path:str) -> None:
        if not os.path.isfile(path):
            raise ValueError("Icorect config path")
        
        config_stream = open(path, "r")
        config = json.load(config_stream)
        self.__scp = config.get("scp", self.__scp)
        self.__SatDump_path = config.get("SatDump_path", self.__baseband_format)
        self.__sdr_name = config.get("sdr_name", self.__sdr_name)
        self.__baseband_format = config.get("baseband_format", self.__baseband_format)
        self.__timeout = config.get("timeout", self.__timeout)
        config_stream.close()

    def load_satellite_config(self, satellite_name: str) -> None:
        path = os.path.join(self.__scp, satellite_name)

        if not os.path.isfile(path):
            raise ValueError("Incoret satelite name")
        
        self.config = Config(path)

    def start_recording(self, record_mode: RecordMode = None) -> None:
        if record_mode is None:
            record_mode = self.default_record_mode
        
        if(record_mode & RecordMode.Raw == RecordMode.Raw):
            Thread(target=self.__start_raw_rec).start()
        
        if(record_mode & RecordMode.Image == RecordMode.Image):
            Thread(target=self.__start_image_rec).start()

    def stop_recording(self) -> None:
        if self.__raw_process is not None:
            self.__raw_process.send_signal(0x03) # CTRL + C signal
        
        if self.__image__process is not None:
            self.__image__process.send_signal(0x03) # CTRL + C signal

    def __start_raw_rec(self) -> None:
        args = [self.__SatDump_path ,"record"]
        args.append(f"'{self.config.satellite_name}:{datetime.utcnow()}'") # output file name
        args.append(f"--source {self.__sdr_name}")
        args.append(f"--samplerate {self.config.samplerate}")
        args.append(f"--baseband_format {self.__baseband_format}")
        args.append(f"--general_gain {self.config.gain}")
        if self.__timeout is not None:
            args.append(f"--timeout {self.__timeout}")
        
        self.__raw_process = Popen(" ".join(args), shell=True)
        self.__raw_process.wait()
        self.__raw_process = None
    
    def __start_image_rec(self) -> None:
        args = [self.__SatDump_path ,"live"]
        args.append(self.config.pipeline)
        args.append(f"'{self.config.satellite_name}:{datetime.utcnow()}'") # output dir name
        args.append(f"--source {self.__sdr_name}")
        args.append(f"--samplerate {self.config.samplerate}")
        args.append(f"--baseband_format {self.__baseband_format}")
        args.append(f"--general_gain {self.config.gain}")
        if self.__timeout is not None:
            args.append(f"--timeout {self.__timeout}")
        
        self.__image__process = Popen(" ".join(args), shell=True)
        self.__image__process.wait()
        self.__image__process = None
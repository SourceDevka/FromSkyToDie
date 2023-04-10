import json

class Config:
    def __init__(self, path: str) -> None:
        file_stream = open(path, "r")
        config = json.load(file_stream)

        self.satellite_name = config["satellite_name"]
        self.pipeline = config["pipeline"]
        self.samplerate = config["samplerate"]
        self.gain = config["gain"]

        file_stream.close()
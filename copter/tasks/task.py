from datetime import datetime

class Task():
    def __init__(self, name: str, args: str, time: datetime = datetime.now(), 
                 isAsync = False) -> None:
        super().__init__()
        self.time = time
        self.name = name
        self.args = args
        self.isAsync = False
    
    def __lt__(self, obj):
        return self.time < obj.time
  
    def __gt__(self, obj):
        return self.time > obj.time
  
    def __le__(self, obj):
        return self.time <= obj.time
  
    def __ge__(self, obj):
        return self.time >= obj.time
  
    def __eq__(self, obj):
        return self.time == obj.time
    
    def __ne__(self, obj):
        return self.time != obj.time

    

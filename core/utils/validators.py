class DataSerializer:
    def __init__(self, data):
        self.data = data
    
    def bool(self):
        if isinstance(self.data, bool):
            return self.data
        elif isinstance(self.data, int):
            return bool(self.data)
        elif isinstance(self.data, str):
            if self.data.lower() in ["true", "1", "t", "y", "yes"]:
                return True
            elif self.data.lower() in ["false", "0", "f", "n", "no"]:
                return False
            else:
                raise ValueError(f"Invalid boolean value [{self.data}]")
        else:
            raise ValueError(f"Invalid boolean value [{self.data}]")
            
        
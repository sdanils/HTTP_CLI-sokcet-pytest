class Request_data:
    def __init__(self):
        self.method: str  = None
        self.url: str = None
        
    def to_bytes(self) -> bytes:
        return None

    @staticmethod
    def from_bytes(binary_data: bytes) -> 'Request_data':
        return Request_data()

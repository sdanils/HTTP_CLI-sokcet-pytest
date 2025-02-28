class Response_data:
    def __init__(self):
        self.method: str  = None
        self.url: str = None
        
    def to_bytes(self) -> bytes:
        return None

    @staticmethod
    def from_bytes(binary_data: bytes) -> 'Response_data':
        return Response_data()
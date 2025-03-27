class ProtocolFactory:
    def __init__(self, protocol: str, data: bytes, time: float):
        self.protocol = protocol
        self.data = data
        self.time = time

    async def float_to_bytes_str(self, time: float) -> bytes:
        return str(time).encode("utf-8")

    async def build(self):
        start_bytes = b"START#"
        protocol = self.protocol.encode("utf-8")
        time = await self.float_to_bytes_str(self.time)

        return start_bytes + protocol + b"DATA#" + self.data + b"TIME#" + time + b"END"



class ProtocolFactory:

    def __init__(self, data: bytes):
        self.data = data

    @property
    async def time(self):
        time = self.data.split(b"TIME#")[-1].split(b"END")[0]
        time = float(time.decode())
        return time

    @property
    async def message(self):
        message = self.data.split(b"DATA#")[-1].split(b"TIME#")[0]
        message = message.decode()
        return message

    @property
    async def protocol(self):
        message = self.data.split(b"START#")[-1].split(b"DATA#")[0]
        message = message.decode()
        return message

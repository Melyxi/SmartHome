import asyncio

from protocol import ProtocolFactory
import RPi.GPIO as GPIO
import time

def radio_443(message: bytes, delay: float):
    bits = [int(bit) for bit in message]
    old_bit = 0
    for bit in bits:
        if old_bit != bit:
            if bit == 1:
                GPIO.output(18, GPIO.HIGH)
            else:
                GPIO.output(18, GPIO.LOW)
        old_bit = bit
        start_time = time.perf_counter()
        while time.perf_counter() - start_time < delay:
            pass


async def handle_echo(reader, writer):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    while True:
        await asyncio.sleep(0.001)
        data = await reader.read(10000)

        if data:
            protocol_factory = ProtocolFactory(data)

            message = data.decode()
            addr = writer.get_extra_info('peername')
            print(f"Received {message!r} from {addr!r}")

            message_time = await protocol_factory.time
            message = await protocol_factory.message
            protocol = await protocol_factory.protocol

            delay = round(message_time / len(message), 6)

            if "RADIO_433MHz" == protocol:
                radio_443(message, delay)

    GPIO.cleanup()


async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8889)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
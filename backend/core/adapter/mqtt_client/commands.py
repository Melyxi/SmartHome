import time


class MqttCommands:
    unacked_publish = set()

    def __init__(self, connection):
        self.connection = connection
        self.connection.user_data_set(self.unacked_publish)

    def wait_message(self, message):
        while len(self.unacked_publish):
            time.sleep(0.01)
        message.wait_for_publish()

    def connect_devices(self, time=254):
        message = self.connection.publish("zigbee2mqtt/bridge/request/permit_join", '{{"time": {}}}'.format(time), qos=1)
        self.unacked_publish.add(message.mid)
        self.wait_message(message)
        return message


    def disable_connect_devices(self):
        self.connection.publish("zigbee2mqtt/bridge/request/permit_join", '{"time": 0}', qos=1)






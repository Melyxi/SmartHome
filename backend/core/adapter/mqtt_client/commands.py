


class MqttCommands:
    unacked_publish = set()

    def __init__(self, connection):
        self.connection = connection
        self.connection.user_data_set(self.unacked_publish)

    def connect_devices(self, time=254):
        message = self.connection.publish("zigbee2mqtt/bridge/response/permit_join", '{"time":%s}' % time, qos=1)

        return message


    def disable_connect_devices(self):
        self.connection.publish("zigbee2mqtt/bridge/response/permit_join", '{"time": 0}', qos=1)


    def send(self):




import paho.mqtt.client as mqtt
from core.configurate_logging import get_logger


server_logger = get_logger("server")

class ClientZigbeeMQTT:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.mqtt_client = self.connect()

    def on_connect(self, client, userdata, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")
        server_logger(f"Connected with result code %s", reason_code)

    def on_message(self, client, userdata, msg):
        print(f"Received message: {msg.topic} {str(msg.payload)}")
        server_logger.info(f"Received message: %s %s", msg.topic, str(msg.payload))


    def connect(self):
        mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        mqttc.on_connect = self.on_connect
        mqttc.on_message = self.on_message
        mqttc.on_publish = self.on_publish

        mqttc.connect(self.host, self.port, 60)
        return mqttc

    def disconnect(self):
        print(f"Client is disconnected")
        server_logger.info(f"Client is disconnected")

    def on_publish(client, userdata, mid, reason_code, properties):
        # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
        try:
            print(f"Publish message: {userdata}")
            server_logger.info("Publish message")
            userdata.remove(mid)
        except KeyError:
            print("on_publish() is called with a mid not present in unacked_publish")
            print("This is due to an unavoidable race-condition:")
            print("* publish() return the mid of the message sent.")
            print("* mid from publish() is added to unacked_publish by the main thread")
            print("* on_publish() is called by the loop_start thread")
            print("While unlikely (because on_publish() will be called after a network round-trip),")
            print(" this is a race-condition that COULD happen")
            print("")
            print("The best solution to avoid race-condition is using the msg_info from publish()")
            print("We could also try using a list of acknowledged mid rather than removing from pending list,")
            print("but remember that mid could be re-used !")

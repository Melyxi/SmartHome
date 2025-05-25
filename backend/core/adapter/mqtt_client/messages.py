from core.extensions import client_mqtt


def handle_mytopic(client, userdata, message):
    # client.subscribe("zigbee2mqtt/bridge/devices")
    client.subscribe("zigbee2mqtt/bridge/event")
    print(f'\n########{"decorator"=}########')
    print(f'\n########{client=}########')
    print(f'\n########{userdata=}########')
    print(f'\n########{message=}########')

client_mqtt.mqtt_client.message_callback_add("zigbee2mqtt/bridge/response/permit_join", handle_mytopic)


def bridge_event(client, userdata, message):
    print("event")
    print(f'\n########{client=}########')
    print(f'\n########{userdata=}########')
    print(f'\n########{message=}########')


client_mqtt.mqtt_client.message_callback_add("zigbee2mqtt/bridge/response/event", bridge_event)


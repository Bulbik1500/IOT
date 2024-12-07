import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# MQTT configuration
MQTT_BROKER = 'broker.emqx.io'  # Replace with your broker's address
MQTT_PORT = 1883
MQTT_TOPIC = 'emqx/esp8266_laby'

# InfluxDB configuration
token = "JvNlsVx9-TNoat_Op6d0GeiQZezk7DnAWhYQj7AdB9sSv65ypZtQYd3qDxbT3aytzTEfxWFLPxjVz71bn4uSNw=="
org = "IOT"
url = "http://localhost:8086"
bucket = "new"  # Replace with the name of your InfluxDB bucket

write_client = InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

# Define the MQTT client callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        temperature = float(msg.payload.decode())
        print(f"Received temperature: {temperature}")

        # Create a data point and write it to InfluxDB
        point = (
            Point("measurement1")
            .tag("tagname1", "tagvalue1")
            .field("field1", temperature)
        )
        write_api.write(bucket=bucket, org=org, record=point)
        print("Data written to InfluxDB.")
    except ValueError as e:
        print("Failed to decode or write data:", e)

# Initialize and run the MQTT client
client_mqtt = mqtt.Client()
client_mqtt.on_connect = on_connect
client_mqtt.on_message = on_message

client_mqtt.connect(MQTT_BROKER, MQTT_PORT, 60)
client_mqtt.loop_forever()

# What is MQTT?
The MQTT protocol is the de-facto standard for IoT messaging. Standardized by OASIS and ISO, MQTT publish/subscribe protocol provides a scalable and reliable way to connect devices over the Internet. Today, MQTT is used by many companies to connect millions of devices to the Internet.
# MQTT_Integration_Example
## Set up venv
Run "bash setup_venv.sh" to create the python environment and install the requirements then reboot the device.
## Sensor Configuration:
### Parameters:
  * "qos": If the subscribing client defines a lower QoS level than the publishing client, the broker will transmit the message with the lower QoS level.
     - At most once (QoS 0)
     - At least once (QoS 1)
     - Exactly once (QoS 2) 
  * "topic": In MQTT, Topic refers to a UTF-8 string that filters messages for a connected client. A topic consists of one or more levels separated by a forward slash (topic level separator).
     - myhome/groundfloor/livingroom/temperature: This topic represents the temperature in the living room of a home located on the ground floor.
     - USA/California/San Francisco/Silicon Valley: This topic hierarchy can track or exchange information about events or data related to the Silicon Valley area in San Francisco, California, within the United States.
     - 5ff4a2ce-e485-40f4-826c-b1a5d81be9b6/status: This topic could be used to monitor the status of a specific device or system identified by its unique identifier.
     - Germany/Bavaria/car/2382340923453/latitude: This topic structure could be utilized to share the latitude coordinates of a particular car in the region of Bavaria, Germany.
  * "host": "10.1.8.247",
  * "port": 1883
### Example:
{
  "qos": 0,
  "topic": "aranet/358151004965/sensors/6009F3/json/measurements",
  "host": "10.1.8.247",
  "port": 1883
}

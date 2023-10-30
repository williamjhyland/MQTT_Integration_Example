# MQTT_Integration_Example
## Set up venv
Run "bash setup_venv.sh" to create the python environment and install the requirements then reboot the device.
## Sensor Configuration:
### Parameters:
  * "qos": If the subscribing client defines a lower QoS level than the publishing client, the broker will transmit the message with the lower QoS level.
     - At most once (QoS 0)
     - At least once (QoS 1)
     - Exactly once (QoS 2) 
  * "topic": "aranet/358151004965/sensors/6009F3/json/measurements",
  * "host": "10.1.8.247",
  * "port": 1883
### Example:
{
  "qos": 0,
  "topic": "aranet/358151004965/sensors/6009F3/json/measurements",
  "host": "10.1.8.247",
  "port": 1883
}

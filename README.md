# MQTT_Integration_Example
## Set up venv
Run "bash setup_venv.sh" to create the python environment and install the requirements then reboot the device.
## Sensor Configuration:
### Parameters:
  * "qos": 0,
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

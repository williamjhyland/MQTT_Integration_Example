# MQTT_Integration_Example/src/__init__.py
from viam.components.sensor import Sensor
from viam.resource.registry import Registry, ResourceCreatorRegistration
from src.MQTT_Client import MQTT_Integration


# Registry.register_resource_creator(Sensor.SUBTYPE, MQTT_Integration.MODEL, ResourceCreatorRegistration(MQTT_Integration.new))
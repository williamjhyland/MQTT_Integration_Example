# MQTT_Integration_Example/src/main.py
import asyncio

from viam.module.module import Module
from viam.components.sensor import Sensor
from viam.resource.registry import Registry, ResourceCreatorRegistration
from viam.logging import getLogger

from src.MQTT_Client import MQTT_Client 
from src.MQTT_Broker import MQTT_Broker 

logger = getLogger(__name__)

thread_mgr = None
viam_mqtt_client = None

async def main():
    """This function creates and starts a new module, after adding all desired resources.
    Resources must be pre-registered. For an example, see the `__init__.py` file.
    """
    Registry.register_resource_creator(Sensor.SUBTYPE, MQTT_Client.MODEL, ResourceCreatorRegistration(MQTT_Client.new))
    Registry.register_resource_creator(Sensor.SUBTYPE, MQTT_Broker.MODEL, ResourceCreatorRegistration(MQTT_Broker.new))
    module = Module.from_args()
    module.add_model_from_registry(Sensor.SUBTYPE, MQTT_Client.MODEL)
    module.add_model_from_registry(Sensor.SUBTYPE, MQTT_Broker.MODEL)
    await module.start()


if __name__ == "__main__":
    asyncio.run(main())
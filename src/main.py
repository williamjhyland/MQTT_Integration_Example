# MQTT_Integration_Example/src/main.py
import asyncio

from viam.module.module import Module
from viam.components.sensor import Sensor
from viam.resource.registry import Registry, ResourceCreatorRegistration
from viam.logging import getLogger

from MQTT_Integration import MQTT_Integration 

from utils import thread_mgr

logger = getLogger(__name__)

thread_mgr = None
viam_mqtt_client = None

async def main():
    """This function creates and starts a new module, after adding all desired resources.
    Resources must be pre-registered. For an example, see the `__init__.py` file.
    """
    Registry.register_resource_creator(Sensor.SUBTYPE, MQTT_Integration.MODEL, ResourceCreatorRegistration(MQTT_Integration.new))
    module = Module.from_args()
    module.add_model_from_registry(Sensor.SUBTYPE, MQTT_Integration.MODEL)
    await module.start()

    try:
        global thread_mgr
        global viam_mqtt_client
        logger.info('starting viam_mqtt_client')

        # setup viam_mqtt_client
        thread_mgr = thread_mgr.get_instance()
        viam_mqtt_client = viam_mqtt_client.get_viam_mqtt_client()
        thread_mgr.spin_and_add_node(viam_mqtt_client)

        module = Module.from_args()
        module.add_model_from_registry(Sensor.SUBTYPE, MQTT_Integration.MODEL)
        await module.start()
    finally:
        thread_mgr.shutdown()



if __name__ == "__main__":
    asyncio.run(main())
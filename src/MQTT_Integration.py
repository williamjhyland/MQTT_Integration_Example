# MQTT_Integration_Example/src/MQTT_Integration.py

import asyncio
from typing import Any, ClassVar, Dict, Mapping, Optional, Sequence, Tuple
from typing_extensions import Self

from viam.components.sensor import Sensor
from viam.operations import run_with_operation
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily
from viam.logging import getLogger

import ssl
import sys
import paho.mqtt.client

import threading

import time

logger = getLogger(__name__)

class MQTT_Integration(Sensor):
    # Subclass the Viam Sensor component and implement the required functions
    MODEL: ClassVar[Model] = Model(ModelFamily("viamlabs","mqtt_integration"), "json")
    topic = None
    host = None 
    port = None
    qos = None
    msg = None
    thread = None
    exit_flag = 0

    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        sensor = cls(config.name)
        sensor.topic = None
        sensor.host = None 
        sensor.port = None
        sensor.qos = None
        sensor.msg = None
        sensor.thread = None
        sensor.reconfigure(config, dependencies)
        return sensor

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        topic = config.attributes.fields['topic'].string_value
        host =config.attributes.fields['host'].string_value
        port = config.attributes.fields['port'].string_value
        qos = config.attributes.fields['qos'].string_value

        if topic == '':
            logger.warning('no topic to listen to...')
        
        if host == '':
            logger.warning('no host to connect to...')
        
        if port == '':
            logger.warning('no port to listen to...')
        
        if qos == '':
            logger.warning('no qos provided...')
        
        logger.info("Config Validated")
        return []

    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        self.exit_flag = 1
        self.topic = config.attributes.fields['topic'].string_value
        self.host =config.attributes.fields['host'].string_value
        self.port = config.attributes.fields['port'].string_value
        self.qos = config.attributes.fields['qos'].string_value
        logger.info("reconfigured... starting thread")
        self.thread = myThread(self, 1, "Thread-1", 1)
        self.thread.message.payload = None
        self.thread.start()

    async def get_readings(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> Mapping[str, Any]:
        try:
            return self.thread.message.payload
        except AttributeError:
            return {
                'Payload': None
            }

class myThread (threading.Thread):
    # create a lock
    lock = threading.Lock()

    message = None

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.aranet_topic = '#'
        self.aranet_qos = 0
        self.running = False
        self.message = {
            'topic': None,
            'payload': None,
            'qos': None
        }

    def run(self):
        print("Starting " + self.name)
        self.running = True
        self.loop()

    def shutdown(self):
        self.running = False

    def on_connect(self, client, userdata, flags, rc):
        # print('connected (%s)' % client._client_id)
        client.subscribe(topic= self.aranet_topic, qos= self.aranet_qos)

    def on_message(self, client, userdata, message):
        # print('------------------------------')
        # print('client: %s' % client)
        # print('userdata: %s' % userdata)
        # print('topic: %s' % message.topic)
        # print('payload: %s' % message.payload)
        # print('qos: %d' % message.qos)
        self.message = message

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def loop(self):
        #while not self.parent.exit_flag:
        client = paho.mqtt.client.Client()
        client.on_connect = self.on_connect
        client.on_subscribe = self.on_subscribe
        client.on_message = self.on_message
        client.connect(host='10.1.5.254', port=1883)
        client.subscribe('aranet/358151004965/sensors/6009F3/json/measurements', 0)
        while self.running:
            client.loop_forever()


# Anything below this line is optional, but may come in handy for debugging and testing.
# To use, call `python wifi_sensor.py` in the command line while in the `src` directory.
async def main():
    print("-----Try Thread Start-----")
    mqtt_client_sensor = MQTT_Integration(name="MQTT_Integration")
    mqtt_client_sensor.thread = myThread(1, "thread", 1)
    mqtt_client_sensor.thread.start()
    print("-----Thread Started-----")
    while True:   
        message = await mqtt_client_sensor.get_readings()
        print("READ....")
        print(message, mqtt_client_sensor, mqtt_client_sensor.thread)
        # print(dir(mqtt_client_sensor))
        print("SLEEP....")
        time.sleep(10)

if __name__ == '__main__':
    asyncio.run(main())
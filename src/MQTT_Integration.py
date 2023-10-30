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
import json

import threading

import time

logger = getLogger(__name__)

class myThread (threading.Thread):
    # create a lock
    lock = threading.Lock()

    def __init__(self, threadID, name, counter, topic, host, port, qos):
        threading.Thread.__init__(self)
        # Thread Info
        self.threadID = threadID
        self.name = name
        self.counter = counter
        # MQTT Info
        self.topic = topic
        self.host = host
        self.port = port
        self.qos = qos
        self.lock = threading.Lock()
        self.running = False
        self.message = {
            'topic': "None",
            'payload': "None",
            'qos': 1,
            'retain': "None"
        }
    


    def run(self):
        # logger.info("Starting " + self.name)
        self.running = True
        self.loop()

    def shutdown(self):
        self.logger.info('shutting down MQTT Client & joining threads')
        self.join()

    def on_connect(self, client, userdata, flags, rc):
        # logger.info('connected (%s)' % client._client_id)
        client.subscribe(topic= self.topic, qos= self.qos)

    def on_message(self, client, userdata, message):
        # logger.info(f'msg: {message}')
        # logger.info(f'msg info: {dir(message)}')
        # print('------------------------------')
        # print('client: %s' % client)
        # print('userdata: %s' % userdata)
        # print('topic: %s' % message.topic)
        # print('payload: %s' % message.payload)
        # print('qos: %d' % message.qos)
        with self.lock:
            self.message = message

    def on_subscribe(self, client, userdata, mid, granted_qos):
        logger.info("Subscribed... ")

    def loop(self):
        client = paho.mqtt.client.Client()
        client.on_connect = self.on_connect
        client.on_subscribe = self.on_subscribe
        client.on_message = self.on_message
        # logger.info('Attempting connection on client to host... %s' % client)
        logger.info('Host: %s' % self.host)
        logger.info('Port: %s' % self.port)
        client.connect(self.host, self.port)
        client.subscribe(self.topic, self.qos)
        # logger.info('Attempting Looping %s' % self.running)
        while self.running:
            client.loop_forever()
        if not self.running:
            client.disconnect()
            self.shutdown()

class MQTT_Integration(Sensor):
    # Subclass the Viam Sensor component and implement the required functions
    MODEL: ClassVar[Model] = Model(ModelFamily("bill","mqtt-subscriber"), "json")
    topic: str
    host: str 
    port: int
    qos: int
    msg: Dict[str, Any]
    thread: myThread
    exit_flag: int

    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        sensor = cls(config.name)
        sensor.topic = None
        sensor.host = None 
        sensor.port = None
        sensor.qos = None
        sensor.thread = None
        sensor.exit_flag = 1
        sensor.reconfigure(config, dependencies)
        return sensor

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        topic = config.attributes.fields['topic'].string_value
        host = config.attributes.fields['host'].string_value
        port = config.attributes.fields['port'].string_value
        qos = config.attributes.fields['qos'].string_value

        qos = config.attributes.fields['matt_test'].string_value

        if topic == '':
            logger.warning('no topic to listen to... use \'#\' as a wild card...')
        
        if host == '':
            logger.warning('no host to connect to...')
        
        if port == '':
            logger.warning('no port to listen to...')
        
        if qos == '':
            logger.warning('no qos provided...')
        
        logger.info("Config Validated")
        return []

    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        self.topic = config.attributes.fields['topic'].string_value
        self.host =config.attributes.fields['host'].string_value
        self.port = int(config.attributes.fields['port'].number_value)
        self.qos = int(config.attributes.fields['qos'].number_value)
        # logger.info("reconfigured... starting thread")
        if self.thread is not None:
            self.thread.join()
        self.thread = myThread(1, "Thread-1", 1, self.topic, self.host, self.port, self.qos)
        self.thread.setDaemon(True)
        self.thread.start()

    async def get_readings(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> Mapping[str, Any]:
        try:
            msg = self.thread.message
            logger.info(msg)
            decodedmsg = msg.payload.decode()            
            try:
                result = json.loads(decodedmsg)
            except:
                print('------------------------------')
                print("A JSON Decode Error Occured... message isn't JSON")
                print('------------------------------')
                result = decodedmsg
            finally:
                # print('------------------------------')
                # print('topic: %s' % msg.topic)
                # print('payload: %s' % msg)
                # print('decoded: %s' % decodedmsg)
                # print('json: %s' % result)
                # print('qos: %d' % msg.qos)
                return {
                    'topic_from_message': msg.topic,
                    'payload': result,
                    'qos': msg.qos,
                    'retain': msg.retain
                    }
        except AttributeError:
            logger.warning("AttributeError... likely no messages received yet...")
            return {
                    'topic_from_message': 'None',
                    'payload': 'None',
                    'qos': 'None',
                    'retain': 'None',
                    }

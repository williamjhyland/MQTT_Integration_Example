# MQTT_Integration_Example/src/MQTT_Integration.py

import asyncio
from typing import Any, ClassVar, Dict, Mapping, Optional, Sequence, Tuple
from typing_extensions import Self
import subprocess
import socket

from viam.components.sensor import Sensor
from viam.components.component_base import ValueTypes
from viam.operations import run_with_operation
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily
from viam.logging import getLogger

import threading


logger = getLogger(__name__)

class myThread (threading.Thread):
    # create a lock
    lock = threading.Lock()

    def __init__(self, threadID, name, port):
        threading.Thread.__init__(self)
        # Thread Info
        self.threadID = threadID
        self.name = name
        self.process = None
        # Broker Info
        self.port = port

    def run(self):
        # logger.info("Starting " + self.name)
        # mosquitto -v -c <path to mosquitto. conf>
        self.process = subprocess.Popen('mosquitto -p ' + str(self.port) +' -v -c mosquitto.conf', shell=True)
        self.running = True

    def shutdown(self):
        self.logger.info('shutting down Mosquitto Broker & joining threads')
        self.process.kill()
        self.join()

class MQTT_Broker(Sensor):
    # Subclass the Viam Sensor component and implement the required functions
    MODEL: ClassVar[Model] = Model(ModelFamily("bill","mqtt-broker"), "mosquitto")
    thread: myThread
    port: int
    exit_flag: int

    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        sensor = cls(config.name)
        sensor.thread = None
        sensor.exit_flag = 1
        sensor.reconfigure(config, dependencies)
        return sensor

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        port = config.attributes.fields['port'].string_value
        if port == '':
            logger.warning('no port to listen to...')
            logger.warning('setting port to default of 1883...')
        return []

    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        # logger.info("reconfigured... starting thread")
        port = config.attributes.fields['port'].string_value
        if port == '':
            self.port = int(1883)
        else:
            self.port = port

        if self.thread is not None:
            self.thread.join()
        self.thread = myThread(1, "Thread-1", 1, self.port)
        self.thread.setDaemon(True)
        self.thread.start()

    async def get_readings(
            self, 
            extra: Optional[Dict[str, Any]] = None, 
            **kwargs
            ) -> Mapping[str, Any]:
        return {
                'Broker Name': 'Mosquitto',
                'Broker IP': socket.gethostbyname(socket.gethostname()),
                'Broker Port': self.port,
                'Process ID': self.thread.process.pid
                }

    async def do_command(
            self,
            command: Mapping[str, ValueTypes],
            *,
            timeout: Optional[float] = None,
            **kwargs
            ) -> Mapping[str, ValueTypes]:
        """
        not implemented right now

        :param command:
        :param timeout:
        :param kwargs:
        :return:
        """
        pass

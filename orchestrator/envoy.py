import time
import docker
from logger import get_logger

logger = get_logger('envoy')


class Envoy:

    def __init__(self):
        self._container_instance = None
        self._fault_type = ''
        self._abort_percentage = 0
        self._delay_percentage = 0
        self._delay_duration_ms = 0

    def _find_envoy_container(self):
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        for container in client.containers.list():
            if container.name == 'envoy':
                return container
        raise ValueError(
            'Container named "envoy" not found. Create one and try again.')

    def _exec(self, command):
        if self._container_instance == None:
            self._container_instance = self._find_envoy_container()
        self._container_instance.exec_run(command)

    def setup_fault(self, fault_type, percentage, duration_ms):
        self._fault_type = fault_type
        if self._fault_type == 'delay':
            self.disable_abort_fault()
            self.enable_delay_fault(duration_ms, percentage)
            time.sleep(0.5)
            logger.info(
                f'setup finished. type delay percentage {self._delay_percentage} duration ms {self._delay_duration_ms}')
        elif self._fault_type == 'abort':
            self.disable_delay_fault()
            self.enable_abort_fault(percentage)
            time.sleep(0.5)
            logger.info(
                f'setup finished. type abort percentage {self._abort_percentage}')

    def enable_delay_fault(self, duration, percentage):
        if percentage != self._abort_percentage or duration != self._delay_duration_ms:
            self._delay_duration_ms = duration
            self._delay_percentage = percentage
            self._exec(f'bash enable_delay_fault.sh {percentage} {duration}')

    def disable_delay_fault(self):
        self._exec(f'bash disable_delay_fault.sh')
        logger.info(f'disabling delay fault')

    def enable_abort_fault(self, percentage):
        if percentage != self._abort_percentage:
            self._abort_percentage = percentage
            self._exec(f'bash enable_abort_fault.sh {percentage}')
            logger.info(f'enabeling abort fault to {percentage}%')

    def disable_abort_fault(self):
        self._exec(f'bash disable_abort_fault.sh')
        logger.info(f'disabling abort fault')

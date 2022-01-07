import docker
import time
from os import environ
from logger import get_logger

logger = get_logger('envoy')

ENVOY_FAULT_INJECTION_PATH = environ.get('ENVOY_FAULT_INJECTION_PATH')

if not ENVOY_FAULT_INJECTION_PATH:
    ENVOY_FAULT_INJECTION_PATH = '.'

class Envoy:

    def __init__(self):
        self._container_instance = None
        self._fault_type = ''
        self._fault_percentage = None
        self._fault_duration = None
        self._fault_status = None

    def _find_envoy_container(self):
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        for container in client.containers.list():
            if container.name == 'envoy':
                return container
        raise ValueError(
            'Container named "envoy" not found!')

    def _exec(self, command):
        if self._container_instance == None:
            self._container_instance = self._find_envoy_container()
        return self._container_instance.exec_run(command)

    def setup_fault(self, fault_spec, percentage):
        if 'type' in fault_spec:
            self._fault_type = fault_spec['type']
            if self._fault_type == 'delay':
                if 'duration' in fault_spec:
                    if percentage != self._fault_percentage or fault_spec['duration'] != self._fault_duration:
                        self.disable_abort_fault()
                        self.enable_delay_fault(fault_spec['duration'], percentage)
                        self._fault_percentage = percentage
                        self._fault_duration = fault_spec['duration']  
                        time.sleep(0.5)
                else:
                    logger.error(f'Missing duration parameter for delay fault!')           
            elif self._fault_type == 'abort':
                if 'status' in fault_spec:
                    if percentage != self._fault_percentage or fault_spec['status'] != self._fault_status:
                        self.disable_delay_fault()
                        self.enable_abort_fault(fault_spec['status'], percentage)
                        self._fault_percentage = percentage
                        self._fault_status = fault_spec['status']  
                        time.sleep(0.5)
                else:
                    logger.error(f'Missing status parameter for abort fault!')  
            else:
                logger.error(f'Fault type {self._fault_type} is not supported!')
        else:
            logger.error(f'Missing fault type!')

    def enable_delay_fault(self, duration, percentage):
        (exit_code, output) = self._exec(f'bash {ENVOY_FAULT_INJECTION_PATH}/enable_delay_fault.sh {percentage} {duration}')
        if exit_code == 0:
            logger.info(f'Enabled {duration} ms delay fault injection in envoy for {percentage}% of requests')
        else:
            logger.error(f'Failed to enable delay fault injection in envoy! {output}')

    def disable_delay_fault(self):
        (exit_code, output) = self._exec(f'bash {ENVOY_FAULT_INJECTION_PATH}/disable_delay_fault.sh')
        if exit_code == 0:
            logger.info(f'Disabled delay fault injection in envoy')
        else:
            logger.error(f'Failed to disable delay fault injection in envoy! {output}')

    def enable_abort_fault(self, status, percentage):
        (exit_code, output) = self._exec(f'bash {ENVOY_FAULT_INJECTION_PATH}/enable_abort_fault.sh {percentage} {status}')
        if exit_code == 0:
            logger.info(f'Enabled {status} abort fault injection in envoy for {percentage}% of requests')
        else:
            logger.error(f'Failed to enable abort fault injection in envoy! {output}')

    def disable_abort_fault(self):
        (exit_code, output) = self._exec(f'bash {ENVOY_FAULT_INJECTION_PATH}/disable_abort_fault.sh')
        if exit_code == 0:
            logger.info(f'Disabled abort fault injection in envoy')
        else:
            logger.error(f'Failed to disable abort fault injection in envoy! {output}')

import requests
from os import environ
from logger import get_logger

logger = get_logger('envoy')

ENVOY_ADMIN_URL = environ.get('ENVOY_ADMIN_URL', 'http://server:9901')

# Runtime keys read by envoy.filters.http.fault
ABORT_PERCENT_KEY = 'fault.http.abort.abort_percent'
ABORT_STATUS_KEY = 'fault.http.abort.http_status'
DELAY_PERCENT_KEY = 'fault.http.delay.fixed_delay_percent'
DELAY_DURATION_KEY = 'fault.http.delay.fixed_duration_ms'

class Envoy:

    def __init__(self):
        self._fault_type = ''
        self._fault_percentage = None
        self._fault_duration = None
        self._fault_status = None

    def _runtime_modify(self, values):
        response = requests.post(f'{ENVOY_ADMIN_URL}/runtime_modify', params=values)
        response.raise_for_status()

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
                else:
                    logger.error(f'Missing duration parameter for delay fault!')
            elif self._fault_type == 'abort':
                if 'status' in fault_spec:
                    if percentage != self._fault_percentage or fault_spec['status'] != self._fault_status:
                        self.disable_delay_fault()
                        self.enable_abort_fault(fault_spec['status'], percentage)
                        self._fault_percentage = percentage
                        self._fault_status = fault_spec['status']
                else:
                    logger.error(f'Missing status parameter for abort fault!')
            else:
                logger.error(f'Fault type {self._fault_type} is not supported!')
        else:
            logger.error(f'Missing fault type!')

    def set_fault(self, fault_spec, percentage):
        """
        Unconditionally sets the fault rate in a single admin call, disabling the other fault type.
        Used to flip faults on and off at time window edges, where setup_fault's caching would skip calls.
        """
        fault_type = fault_spec['type']
        if fault_type == 'delay':
            values = {DELAY_PERCENT_KEY: percentage, DELAY_DURATION_KEY: fault_spec['duration'], ABORT_PERCENT_KEY: 0}
            self._fault_duration = fault_spec['duration']
        elif fault_type == 'abort':
            values = {ABORT_PERCENT_KEY: percentage, ABORT_STATUS_KEY: fault_spec['status'], DELAY_PERCENT_KEY: 0}
            self._fault_status = fault_spec['status']
        else:
            raise ValueError(f'Fault type {fault_type} is not supported!')
        self._runtime_modify(values)
        self._fault_type = fault_type
        self._fault_percentage = percentage

    def enable_delay_fault(self, duration, percentage):
        try:
            self._runtime_modify({DELAY_PERCENT_KEY: percentage, DELAY_DURATION_KEY: duration})
            logger.info(f'Enabled {duration} ms delay fault injection in envoy for {percentage}% of requests')
        except requests.RequestException as e:
            logger.error(f'Failed to enable delay fault injection in envoy! {e}')

    def disable_delay_fault(self):
        try:
            self._runtime_modify({DELAY_PERCENT_KEY: 0})
            logger.info(f'Disabled delay fault injection in envoy')
        except requests.RequestException as e:
            logger.error(f'Failed to disable delay fault injection in envoy! {e}')

    def enable_abort_fault(self, status, percentage):
        try:
            self._runtime_modify({ABORT_PERCENT_KEY: percentage, ABORT_STATUS_KEY: status})
            logger.info(f'Enabled {status} abort fault injection in envoy for {percentage}% of requests')
        except requests.RequestException as e:
            logger.error(f'Failed to enable abort fault injection in envoy! {e}')

    def disable_abort_fault(self):
        try:
            self._runtime_modify({ABORT_PERCENT_KEY: 0})
            logger.info(f'Disabled abort fault injection in envoy')
        except requests.RequestException as e:
            logger.error(f'Failed to disable abort fault injection in envoy! {e}')

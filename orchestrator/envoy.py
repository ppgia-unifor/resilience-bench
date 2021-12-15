import docker
import time
import logging

logger = logging.getLogger('envoy')
logger.setLevel(logging.INFO)

def get_envoy():
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    for container in client.containers.list():
        if container.name == 'envoy':
            return container
    return None    

def update_percentage_fault(percentage):
    envoy = get_envoy()
    envoy.exec_run(f'bash update_percentage_fault.sh {percentage}')
    logging.info(f'update envoy to delay {percentage}% of requests')
    time.sleep(1)

def update_duration_fault(duration):
    envoy = get_envoy()
    envoy.exec_run(f'bash update_duration_fault.sh {duration}')
    logging.info(f'update envoy to delay {duration}ms')
    time.sleep(1)


def update_delay_fault_injection(percentage):
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    for container in client.containers.list():
        if container.name == 'envoy':
            container.exec_run(f'bash update_delay_fault_injection.sh {percentage}')
            logging.info(f'update envoy to delay {percentage}% of requests')
            time.sleep(1)
            
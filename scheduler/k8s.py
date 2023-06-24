from kubernetes import client,config,utils
from kubernetes.client import V1ConfigMap, V1ObjectMeta, V1ConfigMapList, ApiException

class K8s:
    
    def __init__(self):
        config.load_kube_config()
        
        self.__custom_objects = client.CustomObjectsApi()
        self.__core_api = client.CoreV1Api()
        
    
    def get_benchmark(self, name, namespace = "default"):
        return self.__custom_objects.get_namespaced_custom_object(group="resiliencebench.io", version="v1", namespace=namespace, name=name, plural="benchmarks")["spec"]
    
    def update_config_map(self, name, data, namespace = "default"):
        try:
            self.__core_api.delete_namespaced_config_map(name, namespace)
        except ApiException as e:
            if e.status == 404:
                print(f"{name} does not exists. creating a new one")
        cm = V1ConfigMap(immutable=True, data=data, metadata = V1ObjectMeta(name=name))
        self.__core_api.create_namespaced_config_map(namespace=namespace, body=cm)
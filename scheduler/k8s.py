from kubernetes import client,config,utils

class K8s:
    
    def __init__(self):
        config.load_kube_config()
        
        self.__custom_objects = client.CustomObjectsApi()
        
    
    def get_benchmark(self, name, namespace = "default"):
        return self.__custom_objects.get_namespaced_custom_object(group="resiliencebench.io", version="v1", namespace=namespace, name=name, plural="benchmarks")["spec"]
    
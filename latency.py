import requests
import time
from kubernetes import client, config

def increase_replica_set(namespace, deployment_name, replicas):
    config.load_kube_config()
    
    api_instance = client.AppsV1Api()
    
    deployment = api_instance.read_namespaced_deployment(deployment_name, namespace)
    
    deployment.spec.replicas += replicas
    
    api_instance.patch_namespaced_deployment(
        name=deployment_name,
        namespace=namespace,
        body=deployment
    )
    print("Deployment 的 ReplicaSet 已經成功增加！")



def get_api_latency(url):
    start_time = time.time()  
    
    try:
        response = requests.get(url)
        response_time = time.time() - start_time  
        return response_time
      
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

if __name__ == "__main__":
    api_url = "http://10.20.1.2:5000/api/data2"
    
    latency = get_api_latency(api_url)
    if latency > 0.5:
        print("API latency:", latency)
        deployment_name = "python"
        namespace = "default"
        replicas_to_add = 1
    
        increase_replica_set(namespace, deployment_name, replicas_to_add)
    else:
        print("API latency:", latency, "milliseconds")

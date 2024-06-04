import requests
from kubernetes import client, config

def call_api():
    url = 'http://10.20.1.18:5000/api/data'  
    max_d_time = 0
    for i in range(20):
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            name = data["deploy"][0]["name"]
            ns = data["deploy"][0]["namespace"]
            print("Duration Time:", data['d_time'])
            if float(data['d_time']) > max_d_time:
                max_d_time = float(data['d_time'])
        else:
            print("API 調用失敗，狀態碼:", response.status_code)
    print("最高的 d_time:", max_d_time)
    if max_d_time > 3.0:
        deployment_name = name
        namespace = ns
        replicas_to_add = 1
        add = increase_replica_set(namespace, deployment_name, replicas_to_add)
        print("由於最高的d_time > 3.0 ,故增加Deployment的ReplicaSet！")

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

if __name__ == "__main__":
    call_api()
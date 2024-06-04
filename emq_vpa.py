import requests
from kubernetes import client, config


config.load_kube_config()

api_instance = client.AppsV1Api()

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
        new_cpu_request = '400m'
        new_memory_request = '512Mi'

        deployment = api_instance.read_namespaced_deployment(name=deployment_name, namespace=namespace)
        deployment.spec.template.spec.containers[0].resources.requests['cpu'] = new_cpu_request
        deployment.spec.template.spec.containers[0].resources.limits['cpu'] = new_cpu_request
        deployment.spec.template.spec.containers[0].resources.requests['memory'] = new_memory_request
        deployment.spec.template.spec.containers[0].resources.limits['memory'] = new_memory_request

        try:
            api_instance.patch_namespaced_deployment(name=deployment_name, namespace=namespace, body=deployment)
            print("由於最高的d_time > 3.0 ,故擴展Deployment的資源使用量！")
        except Exception as e:
            print("Error updating Deployment:", e)
                


if __name__ == "__main__":
    call_api()
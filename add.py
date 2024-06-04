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

if __name__ == "__main__":
    deployment_name = "python"
    namespace = "default"
    replicas_to_add = 1
    
    increase_replica_set(namespace, deployment_name, replicas_to_add)

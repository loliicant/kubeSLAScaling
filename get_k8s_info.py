from kubernetes import client, config

config.load_kube_config()

v1 = client.CoreV1Api()

print("Nodes in the cluster:")
nodes = v1.list_node().items
for node in nodes:
    print("Node Name: %s\t\tNode Status: %s" % (node.metadata.name, node.status.conditions[-1].type))

print("\nPods in the cluster:")
pods = v1.list_pod_for_all_namespaces().items
for pod in pods:
    print("Pod Name: %s\t\tPod Status: %s\t\tNamespace: %s" % (pod.metadata.name, pod.status.phase, pod.metadata.namespace))

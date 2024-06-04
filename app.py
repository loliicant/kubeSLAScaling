from kubernetes import client, config
from flask import Flask, jsonify
import datetime
import time
import random
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.sdk.resources import Resource

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer("my.tracer.name")

app = Flask(__name__)

#config.load_kube_config()
# 创建 Kubernetes 客户端对象
#v1 = client.CoreV1Api()

#@app.route('/api/info')
#def get_info():
    #node = get_node()
    #pod = get_pod() 
    #return  jsonify({'node_info': node, 'pod_info': pod})

#def get_node():
    #nodes_info = []
    #nodes = v1.list_node().items
    #for node in nodes:
        #nodes_info.append({
            #'name': node.metadata.name,
            #'status': node.status.conditions[-1].type
        #})
    #return nodes_info

#def get_pod():
    #pods_info = []
    #pods = v1.list_pod_for_all_namespaces().items
    #for pod in pods:
        #pods_info.append({
            #'name': pod.metadata.name,
            #'status': pod.status.phase,
            #'namespace': pod.metadata.namespace
        #})
    #return pods_info
######
def get_cluster_info():
    try:
        # 尝试从集群内部加载配置
        config.load_incluster_config()
    except config.config_exception.ConfigException:
        # 如果加载失败，则尝试加载外部 kube-config 文件
        config.load_kube_config()

    # 创建 Kubernetes 的核心 API 客户端
    core_api = client.CoreV1Api()

    # 获取集群信息
    cluster_info = {
        "cluster_name": config.list_kube_config_contexts()[1]["name"],
        "api_server": config.list_kube_config_contexts()[1]["context"]["cluster"]["server"],
        # 可根据需要添加其他信息
    }

    return cluster_info

@app.route('/cluster-info', methods=['GET'])
def cluster_info():
    info = get_cluster_info()
    return jsonify(info)
#@app.route('/api/data')
#def get_data():
    # 模擬隨機延遲時間
    #delay = random.uniform(0.1, 1.0)  # 隨機延遲範圍為 0.1 到 1.0 秒
    #time.sleep(delay)
    
    # 回傳 JSON 資料
    #data = {'message': 'API response with delay of {:.2f} seconds'.format(delay)}
    #return jsonify(data)

@app.route('/api/data2')
def get_data2():
    span = get_span_info()
    start = span.start_time / 1e9  # 將時間戳轉換為秒
    end = span.end_time / 1e9
    tstart = datetime.datetime.fromtimestamp(start)
    tend = datetime.datetime.fromtimestamp(end)
    start_time = tstart.strftime('%Y-%m-%d %H:%M:%S.%f')
    end_time = tend.strftime('%Y-%m-%d %H:%M:%S.%f')
    #print(dir(span.start_time))
    #start_struct = time.localtime(span.start_time/1e9)
    #start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(span.start_time/1e9))
    #end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(span.end_time/1e9))
    dtime = end - start
    d_time = datetime.datetime.fromtimestamp(dtime).strftime("%S.%f")
    span_dict = {
        'name': span.name,
        'start_time': start_time,
        'end_time': end_time,
	'd_time': d_time
    }
    return span_dict 

def get_span_info():
    with tracer.start_as_current_span("test1") as span:
        #span_dict = {
            #'name': span.name,
            #'start_time': span.start_time,
            #'end_time': span.end_time
        #}
        return span
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = '5000')

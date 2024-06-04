import requests
import time

def get_api_latency(url):
    #start_time = time.time()  # 開始計時

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("API請求失敗，狀態碼：", response.status_code)
            return None
        #response_time = time.time() - start_time  # 計算回應時間
        #print(response_time)
        #return response.json

    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

if __name__ == "__main__":
	# 指定 API 的 URL
    api_url = "http://10.20.1.2:5000/api/data2"

    	# 獲取 API 的延遲時間
    latency = get_api_latency(api_url)
    print(latency)

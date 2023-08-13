import requests
import json


timeout_seconds = 3  # 设置超时时间，单位为秒


def check():
    def check_url(url):
        try:
            response = requests.get(url, timeout=timeout_seconds)

            if response.status_code == 200:
                print(f"URL: {url} - 请求成功！")
                print("回显内容：")
                print(response.text)
                with open("./successful_urls.txt", "a") as file:
                    file.write(url + "\n")
                    file.write(response.text+"\n")
                    file.write("-----"+"\n")
            else:
                print(f"URL: {url} - 请求失败，状态码：{response.status_code}")

        except requests.Timeout:
            print(f"URL: {url} - 请求超时。")
        except requests.RequestException as e:
            print(f"URL: {url} - 请求发生异常：{e}")

    # 从文件读取URL并进行遍历检测
    with open(r"./urls.txt", "r") as file:
        for line in file:
            url = line.strip()  # 去除换行符和空格
            if("/cgi-bin/rpc?action=verify-haras" not in url):
                url = url + "/cgi-bin/rpc?action=verify-haras"
            check_url(url)


check()

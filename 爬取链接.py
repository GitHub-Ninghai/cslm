import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# 定义起始和结束编号
start_num = 276747
end_num = 373050

# 定义网址模板
url_template = "https://v.4399pk.com/mobile/cslm/video_{}.htm"

# 创建一个空列表来存储存在的网址
valid_urls = []

# 定义一个函数来检查单个URL
def check_url(num):
    url = url_template.format(num)
    try:
        response = requests.get(url, timeout=5)  # 设置超时时间为5秒
        if response.status_code == 200:
            valid_urls.append(url)
            print(f"编号 {num} 的网址存在。")
        else:
            print(f"编号 {num} 的网址不存在，状态码: {response.status_code}")
    except requests.RequestException as e:
        print(f"编号 {num} 的网址请求失败: {e}")

# 使用ThreadPoolExecutor来并发请求
with ThreadPoolExecutor(max_workers=10) as executor:  # 设置最大线程数为10
    future_to_url = {executor.submit(check_url, num): num for num in range(start_num, end_num + 1)}
    for future in as_completed(future_to_url):
        num = future_to_url[future]
        try:
            # 这将重新引发在future中捕获的异常
            future.result()
        except Exception as exc:
            print(f"编号 {num} 的网址检查生成异常: {exc}")

# 将存在的网址写入TXT文件
with open("valid_urls.txt", "w") as file:
    for url in valid_urls:
        file.write(url + "\n")

print(f"已检查 {end_num - start_num + 1} 个网址，并将 {len(valid_urls)} 个存在的网址写入 valid_urls.txt 文件。")
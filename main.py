import requests
from bs4 import BeautifulSoup
import wget


# 获取以/posts/开头的链接
def get_post_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    post_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith("/posts/"):
            full_link = f"https://danbooru.donmai.us{href}"
            post_links.append(full_link)
    return post_links


# 定义下载函数
def download_images(url, save_path):
    # 获取以/posts/开头的链接
    post_links = get_post_links(url)

    # 下载链接
    for link in post_links:
        try:
            # 发起GET请求获取网页内容
            response = requests.get(link)
            response.raise_for_status()  # 检查请求是否成功

            # 使用BeautifulSoup解析网页内容
            soup = BeautifulSoup(response.text, "html.parser")

            # 查找包含"https://cdn.donmai.us/original/"并包含"download"的链接
            download_links = []
            for a_link in soup.find_all('a', href=True):
                if "https://cdn.donmai.us/original/" in a_link['href'] and "download" in a_link['href']:
                    download_links.append(a_link['href'])

            # 如果找到匹配的下载链接，下载文件到指定路径
            if download_links:
                selected_link = download_links[0]  # 这里选择第一个匹配的链接
                wget.download(selected_link, out=save_path)
                print(f"文件已下载到 {save_path}")
            else:
                print("没有找到匹配的下载链接")
        except requests.exceptions.HTTPError as err:
            print(f"HTTP错误：{err}")
            print(f"下载停止在页码 {page}")
            return


# 输入开始下载和结束下载的页数
start_page = int(input("请输入开始下载的页数: "))
end_page = int(input("请输入结束下载的页数: "))
tag = input("请输入标签: ")

# 逐页下载图片
for page in range(start_page, end_page + 1):
    # 使用页码和标签生成链接
    url = f"https://danbooru.donmai.us/posts?page={page}&tags={tag}"

    # 下载当前页的图片
    download_images(url, r"C:\Users\naras\Downloads")

print("所有图片下载完成。")

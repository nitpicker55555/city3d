import os
import requests
import xmltodict


def download_file(url, filename, download_dir):
    try:
        os.makedirs(download_dir, exist_ok=True)  # 创建下载目录（如果不存在）
        filepath = os.path.join(download_dir, filename)
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 检查请求是否成功
        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"Downloaded {filename} from {url} to {filepath}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {filename} from {url}: {e}")


def parse_meta4(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    meta4_dict = xmltodict.parse(content)
    return meta4_dict['metalink']['file']


def main():
    meta4_file_path = '09162000 (1).meta4'  # 替换为你的meta4文件路径
    download_dir = 'tiles'  # 指定下载目录
    files = parse_meta4(meta4_file_path)

    if not isinstance(files, list):
        files = [files]  # 确保files是一个列表，即使只有一个文件

    for file in files:
        filename = file['@name']
        urls = file['url']

        if not isinstance(urls, list):
            urls = [urls]  # 确保urls是一个列表，即使只有一个URL

        # 尝试下载所有URL中的第一个成功的
        for url in urls:
            download_file(url, filename, download_dir)
            break


if __name__ == '__main__':
    main()

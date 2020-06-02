import requests
from bs4 import BeautifulSoup
import sqlite3

base_url = 'https://www.ygdy8.net/html/gndy/dyzz/list_23_{}.html'

cookies = {
    '37cs_user': '37cs69200568865',
    '37cs_pidx': '2',
    'cscpvrich5041_fidx': '2',
    '37cs_show': '253%2C75',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Referer': 'https://www.dytt8.net/html/dongman/index.html',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'If-None-Match': '"80baba17bac5d51:445"',
    'If-Modified-Since': 'Wed, 08 Jan 2020 00:25:13 GMT',
}

movie = {}

for i in range(1, 6):
    url = base_url.format(i)
    response = requests.get(url, headers=headers, cookies=cookies)
    list_html = response.content.decode('gbk', errors='ignore')

    soup = BeautifulSoup(list_html, 'lxml')
    table_tags = soup.find_all("table", attrs={"class":"tbspan"})
    for table in table_tags:
        a = table.find_all("a")[-1]
        title = a.get_text()
        href = a.get("href")
        detail_url = 'https://www.ygdy8.net/' + href  # 详情页地址
        # print(detail_url)
        response = requests.get(detail_url, headers=headers, cookies=cookies)
        detail_html = response.content.decode('gbk', errors='ignore')
        soup = BeautifulSoup(detail_html, 'lxml')
        div = soup.find_all("div", attrs={"id":"Zoom"})[0]
        imgs = div.find_all("img")[0]  # 海报
        cover_url = imgs.get("src")
        download_url = div.find_all("a")
        # print(download_url[1])
        try:
            thunder_url = download_url[0].get("href")
            magnet_url = download_url[1].get("href")
        except IndexError:
            thunder_url = None
            magnet_url = None
        # 提取文本信息
        try:
            infos = div.find_all("p")[0].get_text()
            datas = infos.split("◎")
        except IndexError:
            datas = []
        for info in datas:
            if info.startswith("类　　别"):
                classify = info.replace("类　　别", "").strip()
                movie['classify'] = classify
            if info.startswith("主　　演"):
                temp = info.replace("主　　演", "").strip()
                actors = temp.replace("\u3000", "")
                movie['actors'] = actors
            if info.startswith("简　　介"):
                content = info.replace("简　　介", "").strip()
                try:
                    index = content.index('【下载地址】')
                    content = content[:index]
                except ValueError:
                    pass
                movie['content'] = content
        classify = movie['classify']
        actors = movie['actors']
        content = movie['content']
        print(f'已爬取电影{title}')

        # 连接到数据库
        conn = sqlite3.connect('blogdata.sqlite')
        sql = 'insert into film(classify, actors, title, content, cover_url, thunder_url, magnet_url) \
                values(?,?,?,?,?,?,?);'
        dt = (classify, actors, title, content, cover_url, thunder_url, magnet_url)
        # 执行sql语句
        conn.execute(sql, dt)
        # 提交到数据库
        conn.commit()
        conn.close()






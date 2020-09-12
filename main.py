import requests
from bs4 import BeautifulSoup
import os

def getpages_HTML(url,info = None):#连接wallhaven随机壁纸页面
    try:
        r = requests.request('GET',url = url,params = info)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("Failed")


def getURL(html,lst):

    soup = BeautifulSoup(html,'html.parser')
    trs = soup.find_all('a')
    for tr in trs:
        if tr.get('href') is not None and len(tr.get('href')) == 29:
            lst.append(tr.get('href'))#提取href


def parseHTML(html):
    
    soup = BeautifulSoup(html,'html.parser')
    img = soup.find_all('img')#解析html页面里的img src标签
    src = img[2].get('src')
    return src #返回.jpg文件下载链接

def getDownload(url,path):
    try:
        r = requests.get(url)
        r.raise_for_status()
        with open(path,'wb')as f:
            f.write(r.content)
    except:
        return "Failed"
    

if __name__ == '__main__':

    pic_dir = 'C://Users//Administrator//Pictures//wallpapers'
    if not os.path.exists(pic_dir):
        os.mkdir(pic_dir)

    infoDict = {}
    lst = []
    page_num = int(input('plese input the page number:'))
    url = 'https://wallhaven.cc/search?categories=110&purity=100&sorting=favorites&order=desc'

    if page_num == 1:#对输入数字进行判断
        infoDict['page'] = 1
        html = getpages_HTML(url = url,info = infoDict)
        getURL(html,lst)
    else:
        for i in range(1,page_num + 1):
            infoDict['page'] = i
            html = getpages_HTML(url = url,info = infoDict)
            getURL(html,lst)

    for i in range(len(lst)):
        pic_html = getpages_HTML(lst[i],info = None)
        downloader = parseHTML(pic_html)
        path = pic_dir + '//' + lst[i][-6:] + '.jpg'
        getDownload(downloader,path)

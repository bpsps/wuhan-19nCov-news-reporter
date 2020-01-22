import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

jilin_urls = ["http://wsjkw.jl.gov.cn/xwzx/xwfb/"]
shanghai_urls = ["http://wsjkw.sh.gov.cn/xwfb/index.html"]
zhejiang_urls = ["http://www.zjwjw.gov.cn/col/col1202101/index.html"]
anhui_urls = ["http://wjw.ah.gov.cn/news_list_450_1.html","http://wjw.ah.gov.cn/news_list_449_1.html"]
henan_urls = ["http://www.hnwsjsw.gov.cn/channels/177.shtml"]
hubei_urls = ["http://wjw.hubei.gov.cn/fbjd/tzgg/"]
guangdong_urls = ["http://wsjkw.gd.gov.cn/zwyw_yqxx/index.html"]
guangxi_urls = ["http://wsjkw.gxzf.gov.cn/gzdt/bt/"]
chongqing_urls = ["http://wsjkw.cq.gov.cn/tzgg/"]
sichuan_urls = ["http://wsjkw.sc.gov.cn/scwsjkw/gggs/tygl.shtml"]
shandong_urls = ["http://wsjkw.shandong.gov.cn/wzxxgk/zwgg/"]
beijing_urls = ["http://wjw.beijing.gov.cn/xwzx_20031/wnxw/"]
shandong_urls = ["http://wsjkw.shandong.gov.cn/wzxxgk/zwgg/"]

def jilin_func():
    #一些基本的信息
    info = "Informations from: %s" % jilin_urls
    news_urls = []
    keywords = ["肺炎","病毒","感染"]
    pacakage = {"info":info}

    for url in select_urls:
        html_page = requests.get(url)
        html_page.encoding = "utf-8"
        soup = BeautifulSoup(html_page.text, 'html.parser')
        news_list = soup.select(".sub_news_list")
        for x in news_list:
            for y in x.select("a"):
                url = y.get("href")[1:]
                title = y.string
                if "ttp://" in url: #判断是不是本站消息
                    pass
                else:
                    url = "http://wsjkw.jl.gov.cn/xwzx/xwfb%s" % url
                    for keyword in keywords: #关键词判断
                        if keyword in title:
                            news_urls.append(url)
                            #print("%s %s" % (title, url))
                            break
    #print(news_urls)
    num = 0
    for url in news_urls:
        num = num + 1
        html_page = requests.get(url)
        html_page.encoding = "utf-8"
        soup = BeautifulSoup(html_page.text, 'html.parser')
        news = soup.select_one(".news")
        title = news.select_one("h3").string
        content = [y.string for y in news.select(".Custom_UnionStyle > p")]
        date = news.select(".news_list_timebar > ul > li:nth-child(2)")[0].string[5:]
        #print("title: %s \ncontent: %s" % (title,content))
        pacakage[num] = {"title":title,"content":content,"date":date}
    pacakage["len"] = num

    return pacakage

def shanghai_func():
    #一些基本的信息
    info = "Informations from: %s" % shanghai_urls
    news_urls = []
    keywords = ["肺炎","病毒","感染"]
    pacakage = {"info":info}

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('log-level=3')
    browser = webdriver.Chrome(chrome_options=options)

    for url in select_urls:
        browser.get(url)
        time.sleep(3)
        news_list = browser.find_element_by_css_selector("#main > div.main-container.margin-top-15 > div > ul").get_attribute("innerHTML")
        news_list = BeautifulSoup(news_list, 'html.parser')
        news_list = news_list.select("li > a")
        for x in news_list:
            url = "http://wsjkw.sh.gov.cn%s" % x.get("href")
            title = x.string
            for keyword in keywords:
                if keyword in title:
                    news_urls.append(url)
                    break
        
    print(news_urls)
    num = 0
    browser = webdriver.Chrome(chrome_options=options)
    browser.set_page_load_timeout(1)
    browser.set_script_timeout(1)#这两种设置都进行才有效
    for url in news_urls:
        num = num + 1
        try:
            browser.get(url)
        except:
            browser.execute_script('window.stop()')
        article = browser.find_element_by_css_selector("div.Article").get_attribute("innerHTML")
        article = BeautifulSoup(article, 'html.parser')
        title = article.select_one("h2").text
        content = [y.text for y in article.select(".Article_content")]
        date = article.select_one(".Article-time").text
        pacakage[num] = {"title":title,"content":content,"date":date[2:12]}
    pacakage["len"] = num
    
    return pacakage

if __name__ == "__main__":
    select_urls = shanghai_urls
    app = shanghai_func()
    print(app)
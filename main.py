import requests
from bs4 import BeautifulSoup

jilin_urls = ["http://wsjkw.jl.gov.cn/xwzx/xwfb/"]
shanghai_urls = ["http://wsjkw.sh.gov.cn/ggl1/index.html","http://wsjkw.sh.gov.cn/xwfb/index.html"]
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

select_urls = jilin_urls

def jilin_func():
    news_urls = []
    keywords = ["肺炎","病毒","感染",]
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
    for url in news_urls:
        html_page = requests.get(url)
        html_page.encoding = "utf-8"
        soup = BeautifulSoup(html_page.text, 'html.parser')
        news = soup.select_one(".news")
        title = news.select_one("h3").string
        content = news.select(".Custom_UnionStyle > p")
        print("title: %s content: %s" % (title,content))

if __name__ == "__main__":
    jilin_func()
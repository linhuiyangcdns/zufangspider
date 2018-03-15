# coding:utf-8
import requests,json,time
from Queue import Queue
import threading
from lxml import etree

class ThreadCrawl(threading.Thread):
    """
    爬取线程
    """
    def __init__(self,crwal_name,page_queue,data_queue):
        super(ThreadCrawl,self).__init__()
        self.crawl_name = crwal_name
        self.page_queue = page_queue
        self.data_queue = data_queue
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive'
        }

    def run(self):
        print("starting" + self.crawl_name)
        while not CRAWL_EXIT:
            try:
                page = self.page_queue.get(False)
                url = "https://www.qiushibaike.com/text/page/"
                full_url = url + str(page) + "/"
                content = requests.get(full_url,headers = self.headers).text
                time.sleep(1)
                self.data_queue.put(content)
            except:
                pass




class ThreadParse(threading.Thread):
    """
    解析线程
    """
    def __init__(self,parse_name,data_queue,filename,lock):
        super(ThreadParse,self).__init__()
        self.parse_name = parse_name
        self.data_queue = data_queue
        self.filename = filename
        self.lock = lock

    def run(self):
        print("strating" + self.parse_name)
        while not PARSE_EXIT:
            try:
                item = self.data_queue.get(False)
                self.parse(item)
            except:
                pass

    def parse(self,item):
        html = etree.HTML(item)
        result_list = html.xpath('//div[contains(@id, "qiushi_tag")]')#使用模糊查找
        for i in result_list:
            name = i.xpath('./div/a/h2/text()')[0].replace("\n","")
            content = i.xpath('./a/div/span/text()')[0].replace("\n","")
            zan = i.xpath('.//i/text()')[0]
            pinglun = i.xpath('.//i/text()')[1]
            item = {
                "name": name,
                "content": content,
                "zan": zan,
                "pinglun": pinglun
            }
            with self.lock:
                self.filename.write(json.dumps(item,ensure_ascii=False).encode("utf-8") + ",\n")

CRAWL_EXIT = False
PARSE_EXIT = False

def main():
    filename = open(r"qsbk.json", "a")
    page_queue = Queue(20)
    for i in range(1, 11):
        page_queue.put(i)
    data_queue = Queue()
    lock = threading.Lock()

    #采集线程
    threadcrawl = []
    crawl_list = ["crawl_1", "crawl_2", "crawl_3"]
    for crawl_name in crawl_list:
        crawl = ThreadCrawl(crawl_name,page_queue,data_queue)
        crawl.start()
        threadcrawl.append(crawl)

    #解析线程
    threadparse = []
    parse_list = ["parse_1","parse_2","parse_3"]
    for parse_name in parse_list:
        parse = ThreadParse(parse_name, data_queue, filename, lock)
        parse.start()
        threadparse.append(parse)

    #
    while not page_queue.empty():
        pass
    global CRAWL_EXIT
    CRAWL_EXIT = True
    for crawl in threadcrawl:
        crawl.join()

    while not data_queue.empty():
        pass
    global PARSE_EXIT
    PARSE_EXIT = True
    for parse in threadparse:
        parse.join()

    with lock:
        filename.close()

if __name__ == "__main__":
    main()











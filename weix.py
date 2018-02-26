# -*- coding:utf-8 -*-

import json,time,requests,random,re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class WeixinSpider():
    def __init__(self):
        self.url = "https://mp.weixin.qq.com"
        self.header = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",

        }
    def land(self):
        """
        作用：获取登录的cookie并保存
        :return:
        """

        #url = "https://mp.weixin.qq.com"
        #dirver = webdriver.PhantomJS()
        driver = webdriver.Chrome()
        driver.get(self.url)
        time.sleep(30)
        #浏览器打开时间
        driver.find_element_by_name("account").clear()
        driver.find_element_by_name("account").send_keys("ps808080@163.com")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("xiaoxiao80")

        driver.find_element_by_xpath('//div[@class="login_btn_panel"]/a[@title="点击登录"]').click()
        time.sleep(10)
        #扫描微信登录帐号
        print("登录成功")
        response = driver.get(self.url)
        #再次发送请求获取cookie和token（微信改造成号接口登录需要）
        token =re.findall(r'token=\d+',str(response.url))[0]
        cookie_items = driver.get_cookie()
        cookie = {}
        for cookie_item in cookie_items:
            cookie[cookie_item['name']] = cookie_item['value']
        cookie_str = json.dumps(cookie)
        with open('cookie.txt', 'w+') as f:
            f.write(cookie_str.encode("utf-8"))
        return token

    def get_content(self,query):
        """
        作用：爬取公众号链接和名称
        :return:
        """
        search_url = "https://mp.weixin.qq.com/cgi-bin/searchbiz?"
        token = self.land()
        query_id = {
            'action': 'search_biz',
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'query': query,
            'begin': '0',
            'count': '5'
        }
        with open('cookie.txt','r') as f:
            cookie = f.read()
        cookies = json.loads(cookie)
        search_response = requests.get(url= search_url,cookies = cookies,headers =self.header,params=query_id)
        # 取搜索结果中的第一个公众号
        lists = search_response.json().get('list')[0]
        # 获取这个公众号的fakeid，后面爬取公众号文章需要此字段
        fakeid = lists.get('fakeid')

        # 微信公众号文章接口地址
        appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
        # 搜索文章需要传入几个参数：登录的公众号token、要爬取文章的公众号fakeid、随机数random
        query_id_data = {
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'action': 'list_ex',
            'begin': '0',
            'count': '5',
            'query': '',
            'fakeid': fakeid,
            'type': '9'
        }
        # 打开搜索的微信公众号文章列表页
        appmsg_response = requests.get(appmsg_url, cookies=cookies, headers=self.header, params=query_id_data)
        # 获取文章总数
        max_num = appmsg_response.json().get('app_msg_cnt')
        # 每页至少有5条，获取文章总的页数，爬取时需要分页爬
        num = int(int(max_num) / 5)
        # 起始页begin参数，往后每页加5
        begin = 0
        while num + 1 > 0:
            query_id_data = {
                'token': token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': '1',
                'random': random.random(),
                'action': 'list_ex',
                'begin': '{}'.format(str(begin)),
                'count': '5',
                'query': '',
                'fakeid': fakeid,
                'type': '9'
            }
            print('正在翻页：--------------', begin)

            # 获取每一页文章的标题和链接地址，并写入本地文本中
            query_fakeid_response = requests.get(appmsg_url, cookies=cookies, headers=self.header, params=query_id_data)
            fakeid_list = query_fakeid_response.json().get('app_msg_list')
            for item in fakeid_list:
                content_link = item.get('link')
                content_title = item.get('title')
                fileName = query + '.txt'
                with open(fileName, 'a') as fh:
                    fh.write((content_title + ":\n" + content_link + "\n").encode('utf-8'))
            num -= 1
            begin = int(begin)
            begin += 5
            time.sleep(2)


if __name__=='__main__':
    try:

        a = WeixinSpider()
        query = raw_input("请输入需要爬取的公众号")
        print("开始爬取公众号：" + query)
        a.get_content(query)
        print("爬取完成")
    except Exception as e:
        print(str(e))
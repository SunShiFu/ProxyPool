import re
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
    }
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def get_page(self,url,headers):

        print('正在抓取', url)
        try:
            response = requests.get(url, headers=headers)
            print('抓取成功', url,response.status_code)
            return response
        except ConnectionError:
            print('抓取失败', url)
            return None

    
    def crawl_ip3366(self):
        #国内高匿
        for i in range(1, 8):
            start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(i)
            response = self.get_page(start_url,self.headers)
            response.encoding = 'gb2312'
            html = response.text
            if html:
                find_tr = re.compile('<tr>(.*?)</tr>', re.S)
                trs = find_tr.findall(html)
                for s in range(1, len(trs)):
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(trs[s])
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(trs[s])
                    for address,port in zip(re_ip_address, re_port):
                        address_port = address+':'+port
                        yield address_port.replace(' ','')

        #国内普通
        for i in range(1, 8):
            start_url = 'http://www.ip3366.net/free/?stype=2&page={}'.format(i)
            response = self.get_page(start_url,self.headers)
            response.encoding = 'gb2312'
            html = response.text
            if html:
                find_tr = re.compile('<tr>(.*?)</tr>', re.S)
                trs = find_tr.findall(html)
                for s in range(1, len(trs)):
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(trs[s])
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(trs[s])
                    for address, port in zip(re_ip_address, re_port):
                        address_port = address + ':' + port
                        yield address_port.replace(' ', '')


    def crawl_89ip(self):
        start_url = 'http://www.89ip.cn'
        response = self.get_page(start_url,self.headers)
        response.encoding = 'utf-8'
        html = response.text
        doc = BeautifulSoup(html, "lxml")
        items = doc.select('.layui-table tbody tr')
        for item in items:
            ip = item.select("td")[0].get_text().strip()
            port = item.select("td")[1].get_text().strip()
            address = ip + ":" + port
            yield address


    def crawl_xicidaili(self):
        for i in range(1, 3):
            start_url = 'http://www.xicidaili.com/wt/{}'.format(i)
            response = self.get_page(start_url,self.headers)
            response.encoding = 'utf-8'
            html = response.text
            if html:
                find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
                trs = find_trs.findall(html)
                for tr in trs:
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(tr)
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(tr)
                    for address,port in zip(re_ip_address, re_port):
                        address_port = address+':'+port
                        yield address_port.replace(' ','')


    def crawl_daili66(self):
        for i in range(1, 35):
            start_url = 'http://www.66ip.cn/areaindex_{}/1.html'.format(i)
            response = self.get_page(start_url,self.headers)
            response.encoding = 'gb2312'
            html = response.text
            doc = BeautifulSoup(html, "lxml")
            items = doc.select('#footer tr')
            for item in items[1:]:
                ip = item.select("td")[0].get_text().strip()
                port = item.select("td")[1].get_text().strip()
                address = ip + ":" + port
                yield address

    def crawl_iphai(self):
        start_url = 'http://www.iphai.com/free/ng'
        response = self.get_page(start_url,self.headers)
        response.encoding = 'utf-8'
        html = response.text
        doc = BeautifulSoup(html,"lxml")
        items = doc.select('.table-responsive tr')
        for item in items[1:]:
            ip = item.select("td")[0].get_text().strip()
            port = item.select("td")[1].get_text().strip()
            address = ip + ":" + port
            yield address


    def crawl_kuaidaili(self):
        for i in range(1, 2):
            start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
            response = self.get_page(start_url,self.headers)
            response.encoding = 'utf-8'
            html = response.text
            doc = BeautifulSoup(html, "lxml")
            items = doc.select('#list tbody tr')
            for item in items:
                ip = item.select("td")[0].get_text().strip()
                port = item.select("td")[1].get_text().strip()
                address = ip + ":" + port
                yield address

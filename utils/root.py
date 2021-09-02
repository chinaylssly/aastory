#_*_ coding:utf-8 _*_

from log import Log
from traceback import format_exc
from bs4 import BeautifulSoup
import requests
from config import PER_REQUESTS_DELAY,PROXIES,IS_CHANGE_HOST,HOST_INDEX,WEBHOSTS
from lxml import etree
import time,re
from faker import Faker

'''
本模块依赖python第三库faker，安装方法 pip install faker
教程详解：https://mp.weixin.qq.com/s/iLjr95uqgTclxYfWWNxrAA
'''
###html5lib 解析需要传入的字符串编码为：Unicode


##随机User-Agent
faker = Faker()

##更换网站域名
reg = reg=re.compile(r'(https://www\.)(.*?)(/.*?)')

class Root(object):

    def __init__(self,url='https://www.aastory.club/category.php',local=None,logger=None,is_change_host=IS_CHANGE_HOST,host_index=HOST_INDEX):

        ##更改网站域名
        if is_change_host:
            url=reg.sub(r'\1%s\3'%(WEBHOSTS[HOST_INDEX]),url)

        self.url=url
        self.local=local
        self.host=self.url.rsplit('/',1)[0]

        if logger is None:
            log = Log()
            logger = log.Logger
        self.logger=logger

        self.get_html()
        # self.get_soup()
        


    def get_html(self,):

        if self.local:
            ##如果存在本地文件，就从本地文件读取html
            
            with open(self.local,'r')as f:
                self.html=f.read()

            self.url=self.local
          
            message=u'load html from localation=%s'%(self.local)
            self.logger.info(message)
            # print message

        else:

            message=u'start requests to %s,then will sleep %s second!'%(self.url,PER_REQUESTS_DELAY)
            self.logger.info(message)
            # print message

            try:
                headers={'User-Agent':faker.user_agent()}
                self.html=requests.get(url=self.url,headers=headers,proxies=PROXIES,timeout=30).content
                self.root=etree.HTML(self.html)
                time.sleep(PER_REQUESTS_DELAY)
            except Exception,e:
                message=u'request url:%s catch exception:%s'%(self.url,e)
                raise Exception,message


    def get_soup(self,):

        if not isinstance(self.html,unicode):
            html=self.html.decode('utf-8','ignore')
        else:
            html=self.html

        self.soup = BeautifulSoup(html, "lxml")
        return self.soup

    @classmethod
    def tostring(self,element):

        return etree.tostring(element)

    @classmethod
    def to_etree(self,html):

        return etree.HTML(html)


def test():

    root=Root()
    print root.html


if __name__ == '__main__':

    test()



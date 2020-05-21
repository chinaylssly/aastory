#_*_ coding:utf-8 _*_

import sys
sys.path.insert(0,'..')

from traceback import format_exc
from utils.root import Root

'''
用于获取某个分类下某一页的书名
'''



class Book(Root):

    def __init__(self,url,local=None,logger=None):

        super(Book,self).__init__(url=url,local=local,logger=logger)


    def get_link(self,):
        ##获取书名及其url

        tags=self.root.findall('.//td[@class="shuming"]//a')

        for tag in tags:

            title=tag.text
            href=tag.get('href')
            tag.get('href')
            url='%s/%s'%(self.host,href)
            id = url.rsplit('=',1)[-1]

            message=u'from category_url=%s,get title=%s,url=%s'%(self.url,title,url)
            self.logger.info(message)
            # print message

            yield dict(title=title,url=url,id=int(id))

    def get_next(self):
        ##获取下一页url

        tags=self.root.findall('.//div[@id="page"]//a')
        href=None
        for tag in tags:
            text=tag.text
            if text ==u'下一页':
                href=tag.get('href')
                break

        if href:

            url=u'%s%s'%(self.host,href)
            message=u'from catrgory_url= %s get next page url =%s'%(self.url,url)

            self.logger.info(message)
            # print message

            return url

        else:

            message=u'cant get next page from url= %s'%(self.url,)
            self.logger.info(message)
            # print message

            return None



def test():

    url='https://www.aastory.club/category.php?t=xuanhuan'
    # url='https://www.aastory.club/category.php?t=gudian'
    # url='https://www.aastory.club/category.php?p=4&t=xuanhuan'
    link=Book(url=url)
    links=link.get_link()
    import json
    for item in links:
        print json.dumps(item,ensure_ascii=False)
    next_url=link.get_next()


if __name__ =='__main__':

    test()
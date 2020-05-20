#_*_ coding:utf-8 _*_

import sys
sys.path.insert(0,'..')
from traceback import format_exc
from utils.root import Root

'''
获取网站分类及其url
'''
class Category(Root):

    def __init__(self,url='https://www.aastory.club/category.php',local=None,logger=None):

        Root.__init__(self,url=url,local=local,logger=logger)


    def get_category(self,):

        # print self.html
        
        tags=self.root.findall('.//div[@class="sub_nav_inner"]//a')

        for tag in tags: 

            title=tag.text
            href=tag.get('href')
            url=u'%s/%s'%(self.host,href)
            message=u'from url=%s get title=%s ,url=%s'%(self.url,title,url)
            self.logger.info(message)
            # print message

            yield dict(title=title,url=url)


            

def test():

    url='https://www.aastory.club/category.php'
    book=Category(url=url)
    category=book.get_category()
    import json
    for item in category:
        print json.dumps(item,ensure_ascii=False)




if __name__=='__main__':

    test()
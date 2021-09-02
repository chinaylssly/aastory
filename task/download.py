#_*_ coding:utf-8 _*_

import sys
sys.path.insert(0,'..')

from traceback import format_exc
from utils.root import Root
import re,os

'''
单个章节下载模块
'''

class Download(Root):

    def __init__(self,url='https://www.aastory.club/read.php?id=201093',local=None,logger=None,filepath=u'book.txt',):

        Root.__init__(self,url=url,local=local,logger=logger)
        self.filepath = filepath
        self.min_size = 300
        #最小下载文件大小，小于这个值，表示未获取到真正的内容,

    def download(self,):
    ##函数返回值为None，表示文件下载失败，返回True，下载完成
        try:

            reg=re.compile(u'chapid.*?&v=(.*?)",')
            result=reg.findall(self.html)

            if result:

                #v为获取内容的必要参数
                v=result[0]
                message=u'from url=%s get v=%s'%(self.url,v)
                self.logger.info(message)
                # print message

                try:
                    contentid = int(self.url.rsplit('=')[-1])
                except:
                    # print self.url
                    contentid = int(self.url.rsplit('-',1)[-1].rsplit('.',1)[0])

                # print contentid
                content_url=u'https://www.aastory.club/_getcontent.php?id=%s&v=%s'%(contentid,v)

                root=Root(url=content_url,logger=self.logger)

                # soup=root.get_soup()
                # text=soup.get_text().strip()

                html=root.html
                text=html.replace('</p>','\n').replace('<p>','').strip()
                text = re.sub(r'<.*?>.*?</.*?>','',text)


                if isinstance(text,unicode):
                    text=text.encode('utf-8','ignore')

                with open(self.filepath,'w')as f:
                    f.write(text)

                # fsize = os.path.getsize(self.filepath)

                # if fsize < self.min_size:
                #     ##小于min_size的文件不保留
                    
                #     os.remove(self.filepath)
                #     message = u'too small filesize,fsize=%s ,remove filepath:%s'%(fsize,self.filepath)
                #     self.logger.debug(message)
                #     return None

                message=u'successfully download file=%s from url:%s'%(self.filepath,self.url)
                self.logger.info(message)
                # print message

                return True


            else:
                ##获取不到必要参数v

                message=u'cant get v from url=%s'%url
                self.logger.debug(message)
                # print message

                return None
        except Exception,e:

            message=u'catch exception when download from url:%s,Exception:%s'%(self.url,e)
            raise Exception,message




def test():
    url = u'https://www.aavbook.fun/read.php?id=200985'
    url = u'https://www.aavbook.fun/read-200978.html'
    download = Download(url=url)
    download.download()




if __name__=='__main__':

    test()


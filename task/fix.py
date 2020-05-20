#_*_ coding:utf-8 _*_

import sys
sys.path.append('..')

from sql.table import Table
import os,json
from utils.config import DOWNLOAD_FOLDER
from utils.tools import Counter,get_filepath
from utils.log import Log



'''
通过analyze函数获取相同大小文件的个数，同样大小的文件很多表示，这些文件很可能是下载失败的文件
可在fix函数中修改fzise_list，删除指定大小的文件
'''

def analyze_error_file(folder,counter=None,min_fsize=2000,miss_fsize=300):
    ##去除下载失败的文件

    kw = dict(counter=counter,min_fsize=min_fsize,miss_fsize=miss_fsize)
    filepaths = get_filepath(folder,is_filter=True,kw=kw)
    for filepath in filepaths:
        
        pass

def analayze():

    folders = [DOWNLOAD_FOLDER,u'f:/data/story']
    counter = Counter()
    for folder in folders[0:1]:
        print folder
        analyze_error_file(folder=folder,counter=counter,)

    print counter.sorted[0:10]


def fix_error_file(table,folder,fsize_list=[],is_test=False):
    ##去除下载失败的文件


    filepaths = get_filepath(folder,is_filter=False,)
    for filepath in filepaths:
        fsize = int(os.path.getsize(filepath))

        if (fsize in fsize_list):
            
            id = filepath.rsplit('\\',1)[-1].split('-',1)[0]
            table.logger.info(json.dumps(dict(filepath=filepath,fsize=fsize,id=id),ensure_ascii=False))
            if is_test:
                pass
            else:
                query = u'update  item set is_download = 0 where id =%s'%(id)
                table.logger.info(query)
                table.execute(query)
                os.remove(filepath)
                message = u'remove filepath:%s'%(filepath)
                table.logger.info(message)


def fix(is_test=False):
    logger = Log(filename=u'fix.log',name ='fix').Logger
    table = Table(logger=logger)

    ignore_list =[63,]
    ##fsize=63，缺失的章节；fsize=36,服务器上的该章节也丢失了
    fsize_list =[1053,36,63,]
    fsize_set = set(fsize_list).difference(set(ignore_list)) 

    folders = [DOWNLOAD_FOLDER,u'f:/data/story']
    for folder in folders:
        print folder
        fix_error_file(folder=folder,table=table,fsize_list=fsize_set,is_test=is_test)

    table.close()


if __name__ =='__main__':

    # fix(True)
    analayze()
    pass
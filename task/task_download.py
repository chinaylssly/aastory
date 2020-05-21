#_*_ coding:utf-8 _*_

import sys
sys.path.append('..')

from download import Download
from sql.table import Table
from utils.log import Log
from utils.config import DOWNLOAD_FOLDER
from task_tool import Task_Tool
import json,os

DOWNLOAD_FOLDER = DOWNLOAD_FOLDER.replace('\\','/')


'''
章节下载
'''





def execute_download(table,queue,logger,is_test=False):
    '''
    核心下载函数
    params: table -> class Table的实例
    params: queue -> book task queue
    params: logger -> Log().Logger
    '''

 
    data = queue.get(block=True,timeout=30)
    category = data.get('category')
    book = data.get('book')
    is_finish = data.get('is_finish')
    id = data.get('id')
    item = data.get('item')
    url = data.get('url')

    if is_finish == 1:
        folder = u'完结'
    else:
        folder = u'连载'

    filefolder = u'%s/%s/%s/%s'%(DOWNLOAD_FOLDER,folder,category,book)

    if not os.path.exists(filefolder):
        os.makedirs(filefolder)
        message = u'makedirs %s'%(filefolder)
        logger.info(message)


    filename = u'%d-%s.txt'%(id,item)
    filepath = u'%s/%s'%(filefolder,filename)

    download = Download(url=url,logger=logger,filepath=filepath)
    
    try:
        flag = download.download()

    except Exception,e:
        
        message = u'catch Exception:%s when execute download,put data:%s back to queue'%(e,json.dumps(data,ensure_ascii=False))
        table.logger.error(message)
        queue.put(data)
        flag = False

    if flag:
        if is_test:
            message = u'update table item set is_downlaod =1 where id =%d'%(id)
            logger.debug(message)
        else:
            table.update_table_item_is_downlaod(id=id)
    else:
        message = u'download file:%s failed'%(filepath)
        logger.debug(message)



    


def task_download(logger,limit=1000,t_n=4,g_sleep=180,g_times=40,e_sleep=10,e_times=30,is_filter=True,is_test=False):
    ##多线程任务函数
    
    task_tool =Task_Tool(logger=logger,is_filter=is_filter)
    generate_func_name = u'check_table_item'
    g_kw = dict(limit=limit)
    e_kw = dict(queue=task_tool.queue,logger=logger,is_test=is_test)

    tasks = task_tool.thread_tasks(generate_func_name=generate_func_name,execute_func=execute_download,g_kw=g_kw,e_kw=e_kw,
                                    t_n=t_n,g_sleep=g_sleep,g_times=g_times,e_sleep=e_sleep,e_times=e_times)
    return tasks




def test_task_download(is_test=True):

    log = Log(filename='download.log',name=u'download')
    logger = log.Logger
    tasks = task_download(logger=logger,is_test=is_test)
    for t in tasks:
        t.start()
    for t in tasks:
        t.join()

if __name__ == '__main__':


    test_task_download()




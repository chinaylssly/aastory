#_*_ coding:utf-8 _*_

import sys
sys.path.append('..')


from utils.log import Log
from utils.config import DOWNLOAD_FOLDER
from sql.table import Table
from task_tool import Task_Tool
import os,json


OLD_DOWNLOAD_FOLDER = u'f:/data/story'

'''
将书本中所有章节合并到同一个文件中
'''



def execute_combine(table,queue,is_test=False,is_cover=False):
    ##合并章节至同一个文件中
    '''
    params: book_dict ->数据
    params: is_cover ->是否覆盖旧文件
    '''
    book_dict =queue.get(block=True,timeout=30)
    book_id = book_dict.get('id')
    book = book_dict.get('book')
    category = book_dict.get('category')
    is_finish = book_dict.get('is_finish')
    if is_finish ==1:
        finish_folder = u'完结'
    else:
        finish_folder = u'连载'

    book_folder = u'%s/combine/%s/%s'%(DOWNLOAD_FOLDER,category,finish_folder)
    if not os.path.exists(book_folder):
        os.makedirs(book_folder)

    book_path = u'%s/%s.txt'%(book_folder,book)
    table.logger.debug(book_path)

    def combine():
        ##合并单个书籍

        if not is_test:
            fb = open(book_path,'w')

        query = u'select id,item from item where book_id =%d order by id asc'%(book_id)
        result_dict = table.execute(query=query)
        data = result_dict.get('data')
        for each in data:
            id = each.get('id')
            item = each.get('item')
            item_name = u'%s-%s.txt'%(id,item)
            old_itempath = u'%s/%s/%s/%s'%(OLD_DOWNLOAD_FOLDER,category,book,item_name)
            itempath = u'%s/%s/%s/%s/%s'%(DOWNLOAD_FOLDER,finish_folder,category,book,item_name)

            if os.path.exists(old_itempath):
                filepath = old_itempath

            if os.path.exists(itempath):
                filepath = itempath
            
            try:
                ##文件目录是否存在
                filepath
            except:
                message = u'cant find item_name:%s,will remove book_path:%s'%(item_name,book_path)
                table.logger.error(message)
                if not is_test:
                    fb.close()
                    os.remove(book_path)
                break

            table.logger.debug(filepath)
            if not is_test:
                itemstr = u'\n%s\n'%(item)
                fb.write(itemstr.encode('utf-8','ignore'))
                with open(filepath) as f:
                    text = f.read()
                fb.write(text)

        if not is_test:
            fb.close()

    if is_cover:
        combine()
    else:
        if os.path.exists(book_path):
            message = u'book_path:%s exists!'%(book_path)
            table.logger.debug(message)
        else:
            combine()

 




def task_combine(logger,t_n=4,g_sleep=180,g_times=1,e_sleep=10,e_times=30,is_filter=True,is_cover=False,is_test=False):
    ##多线程任务函数
    
    def check_table_book_for_combine(self,):
        query = u'select id,book,category,is_finish from book where rate =100'
        return self.execute(query)
    setattr(Table,'check_table_book_for_combine',check_table_book_for_combine)


    task_tool =Task_Tool(logger=logger,is_filter=is_filter)
    generate_func_name = u'check_table_book_for_combine'
    g_kw = {}

    e_kw = dict(queue=task_tool.queue,is_test=is_test,is_cover=is_cover)

    tasks = task_tool.thread_tasks(generate_func_name=generate_func_name,execute_func=execute_combine,g_kw=g_kw,e_kw=e_kw,
                                    t_n=t_n,g_sleep=g_sleep,g_times=g_times,e_sleep=e_sleep,e_times=e_times)
    return tasks




def test_task_combine(t_n=4,is_test=True,is_cover=False):

    log = Log(filename='combine.log',name=u'combine')
    logger = log.Logger
    tasks = task_combine(logger=logger,t_n=t_n,is_test=is_test,is_cover=is_cover)
    for t in tasks:
        t.start()
    for t in tasks:
        t.join()




if __name__ =='__main__':

    test_task_combine(t_n=8,is_test=True,is_cover=False)







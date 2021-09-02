#_*_ coding:utf-8 _*_

import sys
sys.path.insert(0,'..')
from utils.tools import putty
from utils.mysql import MySQL
from sql.table import Table
from utils.log import Log


log = Log(filename='copy.log')
logger = log.Logger
table = Table(logger)
aastory = MySQL(db='aastory',logger=logger)


def copy_item(is_test=False):

    query = u'select id,url,item,book,category,refer,status,finish from item '
    result_dict = aastory.execute(query)
    data = result_dict.get('data')
    for each in data:
        id = each.get('id')
        url = each.get('url')
        item = each.get('item')
        book = each.get('book')
        category = each.get('category')
        refer = each.get('refer')
        status = each.get('status')
        finish = each.get('finish')

        item = putty(item)
        book = putty(book)
        category = putty(category)
        book_id = refer.rsplit('=',1)[-1]

        query = u'insert ignore into item (id,url,item,book,category,book_id,is_download,is_finish) values("%s","%s","%s","%s","%s","%s","%s","%s")'%(id,url,item,book,category,book_id,status,finish)
        if is_test:
            logger.info(query)
        else:
            table.execute(query)



def copy_book(is_test=False):

    query = u'select id,url,book,category,done,total,rate,finish from book '
    result_dict = aastory.execute(query)
    data = result_dict.get('data')
    for each in data:

        id = each.get('id')
        url = each.get('url')
        book = each.get('book')
        category = each.get('category')
        done = each.get('done')
        total = each.get('total')
        rate = each.get('rate')
        finish = each.get('finish')

        book = putty(book)
        category = putty(category)

        query = u'insert ignore into book (id,url,book,category,d_count,total,rate,is_finish) values("%s","%s","%s","%s","%s","%s","%s","%s")'%(id,url,book,category,done,total,rate,finish)
        if is_test:
            logger.info(query)
        else:
            table.execute(query)






def test():
    # copy_book(is_test=False)
    copy_item(is_test=False)
    pass


if __name__ == '__main__':

    table.truncate_table('book')
    table.truncate_table('item')
    copy_book()
    copy_item()

    table.close()
    aastory.close()
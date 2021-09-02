#_*_ coding:utf-8 _*_

import sys
sys.path.insert(0,'..')
from utils.mysql import MySQL



class Table_Book(MySQL):

    def __init__(self,logger=None):
        super(Table_Book,self).__init__(logger=logger)

 
    def create_table_book(self,):
        ##创建Table book
        '''
        column: status(int) value(0 or 1),标识一本书是否下载完了
        column: d_count(int),书籍已下载所有章节数
        column: total(int)， 书籍总章节数
        column: rate(int),value(0 - 100)，书籍已下载章节数占总章目数的百分比,100表示下载完了
        column: finish(int),value(0 or 1), 标识书籍是否完结
        '''

        query='''create table if not exists %s.book(
                id int not null primary key,
                url varchar(100) not null,
                book varchar(50) not null,
                category varchar(20),
                d_count int not null default '0',
                total int not null default '0',
                rate int not null default '0',
                is_finish int not null default '-1',
                create_time timestamp default current_timestamp
                )default charset utf8'''%(self.db)

        self.execute(query=query)


    def check_table_book(self,is_filter=True,rate=100,is_limit=False,limit=20):
        ##查询未下载完全book

        if is_filter:
            filter_str = u'or rate < %s'%(rate)
        else:
            filter_str = u''

        if is_limit:

            limit_str = u'limit %s'%(limit)
        else:
            limit_str = u''

        query='select id,url,book,category,d_count,total from book where is_finish<1 %s order by is_finish asc, rate desc %s'%(filter_str,limit_str)
        return self.execute(query=query)


    def check_table_book_for_timer(self,is_limit=False,limit=100):


        if is_limit:

            limit_str = u'limit %s'%(limit)
        else:
            limit_str = u''

        query='select id,url,book,category,d_count,total from book  order by rate asc, total desc,is_finish asc %s'%(limit_str)
        return self.execute(query=query)



    def check_table_book_for_test(self,):
        ##查询未下载完全book

        query='select id,url,book,category from book limit 1'
        return self.execute(query=query)

    def insert_table_book(self,id,url,book,category):
        ##table book 插入数据

        query='insert ignore into book (id,url,book,category) values("%s","%s","%s","%s")'%(id,url,book,category)
        self.execute(query=query)


    def update_table_book_is_finish(self,is_finish,id):
        ##更新 table book是否完结

        query='update book set is_finish="%s" where id="%s"'%(is_finish,id)
        self.execute(query=query)

    def update_table_book_status(self,d_count,total,rate,book_id):
        ##更新table book d_count,total,rate下载进度信息

        query=u'update book set d_count=%s,total=%s,rate=%s where id="%s"'%(d_count,total,rate,book_id)
        self.execute(query)

    def count_table_book_count_by_category(self,):
        ##查看每一个category下 有多少本book
        
        query=u'select count(*) as book_count,category from book group by category'
        return self.execute(query)


    def check_table_book_url(self,):
        ##用于history.py,与update_table_book_id_by_url一起用于更新id

        query=u'select url from book where id =-1'
        return self.execute(query=query)

    def update_table_book_id_by_url(self,id,url):
        ##用于history.py,与check_table_book一起用于更新id
        
        query=u'update book set id="%d" where url="%s"'%(id,url)
        self.execute(query=query)







def test():

    table_book=Table_Book()
    table_book.create_table_book()
    # table_book.check_table_book()
    


   


if __name__=='__main__':

    test()

    pass





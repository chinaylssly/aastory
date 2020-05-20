#_*_ coding:utf-8 _*_

import sys
sys.path.insert(0,'..')
from utils.mysql import MySQL



class Table_Category(MySQL):

    def __init__(self,logger=None):
        super(Table_Category,self).__init__(logger=logger)

    def create_table_category(self,):
        ##创建table category

        query='''create table if not exists %s.category(
                category varchar(20) not null primary key,
                url varchar(100),
                book_count int not null default '0',
                create_time timestamp default current_timestamp
                )default charset utf8'''%(self.db)

        self.execute(query=query)


    def check_table_category(self,):
        ##查询category url

        query='select category,url from category'
        return self.execute(query=query)



    def insert_table_category(self,category,url):
        ##category 插入数据

        query='insert ignore into category (category,url) values("%s","%s")'%(category,url)
        self.execute(query=query)


    def update_table_category_book_count(self,book_count,category):
        ##更新category book_count

        query='update category set book_count="%s" where category="%s" '%(book_count,category)
        self.execute(query=query)



def test():

    table_category=Table_Category()
    table_category.create_table_category()


   


if __name__=='__main__':

    test()

    pass





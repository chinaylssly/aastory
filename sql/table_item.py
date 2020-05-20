#_*_ coding:utf-8 _*_

import sys
sys.path.insert(0,'..')
from utils.mysql import MySQL



class Table_Item(MySQL):

    def __init__(self,logger=None):
        super(Table_Item,self).__init__(logger=logger)

 
    def create_table_item(self,):
        '''
        column: is_download(int) value(0 or 1)，标识章节是否已下载
        '''

        query='''create table if not exists %s.item(
                id int not null primary key,
                url varchar(100) not null,
                item varchar(50)not null,
                book varchar(50),
                category varchar(20),
                book_id int not null,
                is_download int not null default '0',
                is_finish int not null default '-1',
                create_time timestamp default current_timestamp
                )default charset utf8'''%(self.db)

        self.execute(query=query)



    def insert_table_item(self,id,url,item,book,category,book_id,is_finish):
        ##table item 插入数据

        query = 'insert ignore into item (id,url,item,book,category,book_id,is_finish) values("%s","%s","%s","%s","%s","%s","%s")'%(id,url,item,book,category,book_id,is_finish)
        self.execute(query=query)


    def check_table_item(self,limit=1000):
        '''
        查询未下载item，limit为限制条数，默认1000，若不以限制limit设置为满足bool(limit) is False
        '''

        if limit:
            limitstr = u'limit %d'%(limit)
        else:
            limitstr = u''
        
        query=u'select id,url,book,category,item,is_finish from item where is_download=0 %s'%(limitstr)
        return self.execute(query=query)

    def update_table_item_is_downlaod(self,id,is_download=1):
        ##根据id更新item下载状态

        query='update item set is_download="%s" where id="%s"'%(is_download,id)
        self.execute(query=query)

    def check_table_item_download_path(self,id):
        ##根据id查询item的下载路径,用于确认文件是否已下载

        query=u'select category,book,item,is_finish from item where id="%s'%(id)
        return self.execute(query)

    def count_table_item_total_by_book_id(self,book_id,is_download=-1):
        ##查询一本书下章目数 is_download =0,查询未下载章节数；is_download =1,查询已下载章节数;其他值，查询全部章节数

        if is_download == 1 or is_download == 0:
            is_download_str = u'and is_download = %d'%(is_download)
        else:
            is_download_str = u''

        query='select count(*) as total from item where book_id=%s %s'%(book_id,is_download_str)
        result = self.execute(query)
        return result.get('data')[0].get('total')

    


    def check_table_item_url(self,):
        ##用于history.py,与update_table_item_id_by_url一起用于更新id

        query=u'select url from item where id =-1'
        return self.execute(query=query)

    def update_table_item_id_by_url(self,id,url):
        ##用于history.py,与check_table_item一起用于更新id
        
        query=u'update item set id="%d" where url="%s"'%(id,url)
        self.execute(query=query)




def test():

    table_item=Table_Item()
    table_item.create_table_item()

   


if __name__=='__main__':

    test()

    pass





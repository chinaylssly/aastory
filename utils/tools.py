#_*_ coding:utf-8 _*_
import re,os



def putty(path):
    '''
    美化路径，便于创建文件夹
    '''

    path=path.strip()
    path=path.replace('\r',' ').replace('\n',' ').replace('\t',' ').replace('/','-').replace('\\','-').replace('?','')
    path=path.replace('<','(').replace('>',')').replace('|','-').replace(':',' ').replace('"',' ').replace('*',' ')
    reg=re.compile(' +')
    path=reg.sub(' ',path)
    return path



class Counter(dict):
    ##计数器，


    def __init__(self,):
          
        super(Counter,self).__init__()
    
    def __call__(self,key):

        if self.get(key):
            self[key] = self[key] +1
        else:
            self[key] = 1

    @property
    def sorted(self,):
        return sorted(self.items(),key=lambda iters:iters[1],reverse=True)




def get_filepath(folder,is_filter=False,kw={}):
    ##获取文件夹下所有文件,filter_func为过滤函数

    for dirpath,dirname,filenames in os.walk(folder):
        if not dirname:
            for filename in filenames:
                filepath = os.path.join(dirpath,filename)
                if is_filter:
                    if Filter(filepath,**kw).filter():
                        yield filepath
                    else:
                        pass
                else:
                    yield filepath




class Filter(object):

    def __init__(self,filepath,counter=None,min_fsize=2000,miss_fsize=200,keywords=[u'缺']):
        self.filepath = filepath
        self.counter  = counter
        self.min_fsize = min_fsize
        self.miss_fsize = miss_fsize
        self.keywords = keywords

    def filter_text(self,):

        if self.keywords :
            with open(self.filepath,'r')as f:
                text = f.read().decode('utf-8','ignore')

            for keyword in self.keywords:
                if keyword in text:
                    self.flag = False
                    break
                else:
                    self.flag = True
        else:
            self.flag = True


    def filter(self,):
        ##过滤函数

        fszie = os.path.getsize(self.filepath)
        if fszie < self.miss_fsize:
            self.filter_text()
        elif fszie < self.min_fsize and fszie > self.miss_fsize:
            self.flag = True
        else:
            self.flag = False

        if self.flag:
            self.counter(int(fszie))

        return self.flag






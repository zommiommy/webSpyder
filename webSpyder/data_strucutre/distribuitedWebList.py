

from functools import reduce
from webSpyder.data_strucutre.data_interface import DataInterface
from webSpyder.files_function import check_file_existance,create_file

class DistribuitedWebList(DataInterface):
    n_of_pages = 0
    n_of_chunk = 8
    unparsed_symbol = "U"
    parsed_symbol = "P"
    symbols_len = 1
    fp_list = []

    def hash(self,value):
        values = map(lambda x: ord(x),list(value))
        sum = reduce((lambda x, y: x + y), values)
        return sum%self.n_of_chunk

    def __init__(self,logger,settings):
        self.logger = logger
        self.settings = settings
        self.create_files()
        self.create_fp_list()

    def create_files(self):
        for i in range(self.n_of_chunk):
            self.check_and_create_file(i)

    def check_and_create_file(self,i):
        name = self.settings.get_state_path()+"%d.txt"%i
        if check_file_existance(self.settings.get_state_path(),"%d.txt"%i) == False:
            self.logger.info("the file %s does not exist so now it will be created"%name)
            create_file(name)

    def create_fp_list(self):
        self.fp_list = []
        for i in range(self.n_of_chunk):
            self.fp_list.append(open(self.settings.get_state_path()+"%d.txt"%i,"r+"))

    def close_fp_list(self):
        for f in self.fp_list:
            f.flush()
            f.close()

    def __str__(self):
        stringa = ""
        for i,f in enumerate(self.fp_list):
            stringa += "\n\nChunk #%d\n"%i
            f.seek(0,0) #Start of file
            temp = str(f.read()).split("\n")
            for line in temp:
                stringa += line[self.symbols_len:] + "\n"
        return stringa

    def __len__(self):
        return self.n_of_pages

    def __contains__(self,item):
        h = self.hash(item)
        fp = self.fp_list[h]

        for line in fp:
            if item == line[self.symbols_len:-1]:# line have the \n at the end
                return True
        return False

    def set_and_update_cost(self,link,cost):
        return None

    def add_node(self,father,link):
        if self.__contains__(link):
            self.logger.info("The url %s already exist"%link)
            return

        h = self.hash(link)
        self.logger.info("Adding to the %d chunk %s"%(h,link))
        fp = self.fp_list[h]
        fp.seek(0,2)# End of the file
        fp.write(self.unparsed_symbol+str(link)+"\n")
        self.n_of_pages += 1

    def add_root(self,link):
        if link == "" or link == None:
            return
        self.add_node("",link)

    # TODO Scriverlo Decentemente
    def get_next_page(self):
        found = 0
        for i,f in enumerate(self.fp_list):
            f.seek(0,0) # Start of the file
            last_position = 0
            lines = f.read().split("\n")
            for line in lines:
                if line not in ["",None] and line[0] == self.unparsed_symbol:
                    found = 1
                    break
                else:
                    last_position += len(line)
            if found == 1:
                break

        if found == 1:
            f.seek(last_position,0)#come back to the start of the line
            f.write(self.parsed_symbol)
            return line[1:]
        else:
            return None

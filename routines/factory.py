from plugins import get_plugin
from utils import Walker
from collections import defaultdict

class Resource:

    def __init__(self, *, scheme: str, host: str):

        pcl = get_plugin(scheme)
        self.walker = Walker(pcl(host)) 

    def new_collection(self, pathname, data_dir, idx_rgx="^[A-Z0-9]{7}$"):
        """create a data collection from an index directory and target data path. 
        A collection is a series of buckets storing uniform sets of data mapping to 
        a specific index (i.e., SampleID). All directory names listed in the index 
        directory will be treated as the index ID, and all files immediately contained 
        in the data directory (or multiple directories matched after unix-style shell-expansion) 
        will be stored in the bucket for the given index. No files contained in subdirectories 
        of the data directories will be used.""" 

        counter = 0
        d=defaultdict(list)
        for idxpath in self.walker.scandirs(pathname, idx_rgx):
            dirname, idx = self.walker._split(idxpath)
            counter+=1
            print("Resource.new_collection: Creating bucket for index '{0}', total={1} ".format(idx, counter), flush=True)
            for ddir in self.walker.find(idxpath, data_dir):
                print(f"Resource.new_collection: Searching {ddir}")
                for record in self.walker.getfiles(self.walker._join(idxpath, ddir)):
                    d[idxpath].append(record)

            if counter==5: break

        return d
 
    def _new_collection(self, pathname, data_dir, idx_rgx="^[A-Z0-9]{7}$"):
        index = self.walker.scandirs(pathname, idx_rgx)
        if index:
            last = ','.join(index[-5:])
            print("Resource.new_collection: Creating new collection with {0} indices {1}...{2}".format(len(index), index[0], last))
        else:
            print("No indices found in {} matching regex={}".format(pathname, idx_regex))

        return index

        

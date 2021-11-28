from plugins import get_plugin
from utils import Walker

class Resource:

    def __init__(self, *, scheme: str, host: str):

        pcl = get_plugin(scheme)
        self.cl = Walker(pcl(host)) 

    def new_collection(self, pathname, data_dir, idx_rgx="^[A-Z0-9]{7}$"):
        index = self.cl.scandirs(pathname, idx_rgx)
        if index:
            last = ','.join(index[-5:])
            print("Resource.new_collection: Creating new collection with {0} indices {1}...{2}".format(len(index), index[0], last))
        else:
            print("No indices found in {} matching regex={}".format(pathname, idx_regex))

        return index

        

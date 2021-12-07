import json
from collections import namedtuple

Params = namedtuple('Parts', 'user, scheme password host path port', 
                defaults=["anonymous", 'ftp', None, None, None, None])

def read_config(path):
    cfg = read_json(path)
    params = get_params(cfg)
    return params

def read_json(path):

    with open(path, 'r') as fh:
        dat = json.loads(fh.read())
        return dat 

def dump_json(d, outfile):

    with open(outfile, "w") as fh:
        json.dump(d, fh)

def get_params(config):
    params = Params()._asdict()
    for k,v in config.items():
        if k in params.keys():
            params[k]=v

    return(params)




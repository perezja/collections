import argparse
import json

from collections import namedtuple

from plugins import *

Params = namedtuple('Parts', 'user, scheme password host path port', 
                defaults=["anonymous", 'ftp', None, None, None, None])

def get_params(config):
    params = Params()._asdict()
    for k,v in config.items():
        if k in params.keys():
            params[k]=v

    return(params)

parser = argparse.ArgumentParser()
parser.add_argument('config')
parser.add_argument('--path', default=None)
parser.add_argument('--loglevel', default='INFO')
args = parser.parse_args()

def main(args):

    from uri import URI

    with open(args.config, 'r') as ip:
        config = json.loads(ip.read())
   
    # initialize resource URI
    params=get_params(config)
    if args.path:
        params['path'] = args.path

    uri = URI(**params)

    # get protocol handler for resource
    pcl = get_plugin('ftp')
    assert issubclass(pcl, ProtocolInterface)

    handler = pcl(config['host'])

    result = handler.ls(params.get('path'))
    print(result)

if __name__ == "__main__":
    main(args)


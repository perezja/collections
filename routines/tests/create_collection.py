import json

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('config')
    parser.add_argument('--loglevel', default='INFO')
    args = parser.parse_args()
    
    with open(args.config, 'r') as ip:
        config = json.loads(ip.read())
        print(config)

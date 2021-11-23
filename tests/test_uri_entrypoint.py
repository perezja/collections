import uri 
from pkg_resources import iter_entry_points
from uri.scheme import URLScheme
from uri.part.scheme import SchemePart

def get_schemes():
    schemes = {} 
    for scheme in iter_entry_points('uri.scheme'):
        schemes[scheme.name] = scheme.load()
    return schemes 
def scheme_plugin(plugin):
    pl, = iter_entry_points('uri.scheme', plugin)
    print(pl.__dict__)
    sch = pl.load()
    print(sch.__dict__)
    print(dir(sch))

def scheme_part():
    ncbi="ftp-trace.ncbi.nlm.nih.gov//1000genomes/ftp/phase3/data/HG00154/sequence_read"
    print("url={}".format(ncbi))
    _uri = uri.URI 
    #print("URI.scheme.is_relative", _uri.scheme.is_relative)
    # AttributeError: 'SchemePart' object has no attribute 'is_relative'
    u=uri.URI(ncbi)
    print(type(u))
    print("URI(url).scheme", u.scheme)

    ncbi2="ftp.ncbi.nlm.nih.gov//1000genomes/ftp/phase3/data/HG00154/sequence_read"
    print("url={}".format(ncbi2))
    u=uri.URI(ncbi2)
    print(dir(u))
    print("URI(url).scheme: ", u.scheme)
    print("URI(url).scheme.is_relative: ", u.scheme.is_relative())

if __name__ == "__main__":
   sch = get_schemes()
   #print(sch)
   plugin='ftp'
   #scheme_plugin(plugin)
   scheme_part()




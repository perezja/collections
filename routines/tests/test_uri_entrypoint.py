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
    sch.is_relative()
    print(sch.__dict__)
    print(dir(sch))


if __name__ == "__main__":
   sch = get_schemes()
   #print(sch)
   plugin='ftp'
   scheme_plugin(plugin)




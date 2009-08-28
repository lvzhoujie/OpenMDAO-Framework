
"""
Manages the creation of framework objects, either locally or remotely.
"""


#public symbols
__all__ = [ "create", "register_factory", "get_available_types" ]


import os

from openmdao.main.importfactory import ImportFactory
from openmdao.main.pkg_res_factory import PkgResourcesFactory

_factories = []
search_path = []

# this list should contain all openmdao entry point groups for Containers
_container_groups = [ 'openmdao.container',
                      'openmdao.component',
                      'openmdao.driver',
                    ]

def create(typname, version=None, server=None, res_desc=None, **ctor_args):
    """Create and return an object specified by the given type, name,
    version, etc.
    """
    obj = None
    for fct in _factories:
        obj = fct.create(typname, version, server, res_desc, **ctor_args)
        if obj is not None:
            return obj
    
    raise NameError("unable to create object of type '"+typname+"'")


def register_factory(fct):
    """Add a Factory to the factory list."""
    if fct not in _factories:
        _factories.append(fct)      
          
def get_available_types(groups=None):
    """Return a set of tuples of the form (typename, dist_version), one
    for each available plugin type in the given entry point groups.
    If groups is None, return the set for all openmdao entry point groups.
    """
    if groups is None:
        groups = _container_groups
    types = []
    for fct in _factories:
        types.extend(fct.get_available_types(groups))
    return types


# register factory for simple imports
register_factory(ImportFactory())

# register factory that loads plugins via pkg_resources
pluginpath = os.environ.get('OPENMDAO_PLUGIN_PATH')
if pluginpath:
    if ';' in pluginpath or ':\\' in pluginpath:
        pluginpath = pluginpath.split(';')
    else:
        pluginpath = pluginpath.split(':')
    register_factory(PkgResourcesFactory(groups=_container_groups, 
                                         search_path=pluginpath))
else:
    top = os.environ.get('OPENMDAO_TOP')
    if top and os.path.isdir(os.path.join(top,'plugins')):
        register_factory(PkgResourcesFactory(groups=_container_groups,
                                             search_path=os.path.join(top,'plugins')))
    else:
        register_factory(PkgResourcesFactory(groups=_container_groups))

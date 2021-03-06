"""
Trait for a Slot meant to contain an object of a particular type
or having a particular interface (either a Traits interface or a
zope.interface).  
"""

# The regular Instance class that comes with Traits will only check public
# methods on an object if that object is not a HasTraits object, which means
# we get essentially no error checking for things like Case iterators where
# their API doesn't include any public methods. If we use zope.interface we
# don't have this problem.

#public symbols
__all__ = ["Slot"]

# pylint: disable-msg=E0611,F0401
from enthought.traits.api import Instance, Interface
import zope.interface

from openmdao.main.variable import Variable

class Slot(Variable):
    """A trait for an object of a particular type or implementing a particular
    interface. Both Traits Interfaces and zope.interface.Interfaces are
    supported.
    """
    
    def __init__(self, klass = None, allow_none = True, factory = None, 
                 args = None, kw = None, **metadata):
        try:
            iszopeiface = issubclass(klass, zope.interface.Interface)
        except TypeError:
            iszopeiface = False
        
        metadata.setdefault( 'copy', 'deep' )

        self._allow_none = allow_none
        self.klass = klass
        default_value = None

        if iszopeiface:
            self._instance = None
            self.factory = factory
            self.args = args
            self.kw = kw
        else:
            self._instance = Instance(klass=klass, allow_none=allow_none, 
                                      factory=factory, args=args, kw=kw,
                                      **metadata)
            default_value = self._instance.default_value
        super(Slot, self).__init__(default_value, **metadata)

    def validate ( self, obj, name, value ):
        """ Validates that the value is a valid object instance."""
        if value is None:
            if self._allow_none:
                return value
            self.validate_failed( obj, name, value )

        if self._instance is None:  # our iface is a zope.interface
            if self.klass.providedBy(value):
                return value
            else:
                self._iface_error(obj, name, self.klass.__name__)
        else:
            try:
                return self._instance.validate(obj, name, value)
            except Exception:
                if issubclass(self._instance.klass, Interface):
                    self._iface_error(obj, name, self._instance.klass.__name__)
                else:
                    obj.raise_exception("%s must be an instance of class '%s'" %
                                        (name, self._instance.klass.__name__), 
                                        TypeError)

    def _iface_error(self, obj, name, iface_name):
        obj.raise_exception("%s must provide interface '%s'" % 
                            (name, iface_name), TypeError)
        
"""
A driver is used to run a workflow in an assembly.
"""

#public symbols
__all__ = ["Driver"]

__version__ = "0.1"


from zope.interface import implements

from openmdao.main.interfaces import IDriver, IVariable
from openmdao.main.component import Component, STATE_WAITING, STATE_RUNNING


class Driver(Component):
    """ A driver is used to run a workflow in an assembly. """
    
    implements(IDriver)

    def __init__(self, name, parent=None, desc=None):
        Component.__init__(self, name, parent, desc)

        
    def execute(self):
        """ Run the assembly by invoking run() on the workflow. """
        self.state = STATE_WAITING
        status = self.parent.workflow.run()
        self.state = STATE_RUNNING
        return status

        
    def stop(self):
        """ Stop the assembly by stopping the workflow. """
        self._stop = True
        self.parent.workflow.stop()
        
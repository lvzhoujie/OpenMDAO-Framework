""" 
Pseudo package containing all of the main classes/objects in the 
openmdao.main API.

"""

from openmdao.util.log import logger, enable_console
from openmdao.main.expreval import ExprEvaluator

from openmdao.main.factory import Factory
from openmdao.main.factorymanager import create, get_available_types

from openmdao.main.container import Container, set_as_top, get_default_name, \
                                    create_io_traits
from openmdao.main.component import Component, SimulationRoot
from openmdao.main.component_with_derivatives import ComponentWithDerivatives
from openmdao.main.driver_uses_derivatives import DriverUsesDerivatives
from openmdao.main.assembly import Assembly, dump_iteration_tree
from openmdao.main.driver import Driver
from openmdao.main.workflow import Workflow
from openmdao.main.dataflow import Dataflow
from openmdao.main.seqentialflow import SequentialWorkflow
from openmdao.main.variable import Variable
from openmdao.main.slot import Slot

from openmdao.main.exceptions import ConstraintError

from openmdao.main.filevar import FileMetadata, FileRef

from openmdao.main.case import Case

from openmdao.main.arch import Architecture

from openmdao.util.eggsaver import SAVE_YAML, SAVE_LIBYAML, \
                                   SAVE_PICKLE, SAVE_CPICKLE

from openmdao.units import convert_units

from zope.interface import implements, Attribute, Interface

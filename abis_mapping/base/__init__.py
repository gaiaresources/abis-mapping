"""Exports sub-package interface"""

# Local
from . import mapper
from . import loader
from . import types

# bypass the frictionless memory limit when validating a Resource (e.g. a CSV)
# the default setting is 1000MB but the way frictionless evaluate memory usage is a bit dodgy.
# It checks the memory of the whole process.
# see https://github.com/frictionlessdata/framework/blob/main/frictionless/helpers.py#L385
# and https://github.com/frictionlessdata/framework/blob/v4/frictionless/resource/validate.py#L119
# The annoying thing: it seems they dropped this memory check in the V5 and this memory limit will become incompatible.
# At the time of writing (16/11/2022) # V5 is in beta
FRICTIONLESS_LIMIT_MEMORY = 0

#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")


name = "CodeEditor"
default_task = "publish"


@init
def set_properties(project):
    pass

#   -*- coding: utf-8 -*-
from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")


name = "Sim_Replay"
default_task = "publish"


@init
def set_properties(project):
    project.build_depends_on("mockito")
    project.set_property('dir_source_unittest_python', './')
    project.set_property('source_dist_ignore_patterns',["*.pyc", ".hg*", ".svn", ".CVS","target/*"])

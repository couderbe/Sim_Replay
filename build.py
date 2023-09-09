#   -*- coding: utf-8 -*-
from subprocess import call
from pybuilder.core import use_plugin, init, task, after, Project

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")


name = "Sim_Replay"
default_task = "publish"


@init
def set_properties(project:Project):
    project.build_depends_on("mockito")
    project.set_property('dir_source_unittest_python', './')

@after("run_unit_tests", only_once=True)
def behave(project):
    call(["behave","--color"])
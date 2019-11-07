#!/usr/bin/env python
#
# License: BSD
#   https://raw.githubusercontent.com/splintered-reality/py_trees/devel/LICENSE
#

##############################################################################
# Imports
##############################################################################

import py_trees
import py_trees.console as console

##############################################################################
# Logging Level
##############################################################################

py_trees.logging.level = py_trees.logging.Level.DEBUG
logger = py_trees.logging.Logger("Nosetest")

##############################################################################
# Tests
##############################################################################

# Note: these tests are inspired from the script posted here:
# https://github.com/splintered-reality/py_trees/issues/50

def test_chooser_memory():
    console.banner("Chooser with Memory")
    chooser = py_trees.composites.ChooserWithMemory(name="Memory chooser")
    tree = create_tree(chooser, "immediate-failure")
    tick_four_times(tree)
    assert(tree.status == py_trees.common.Status.SUCCESS)

    chooser = py_trees.composites.ChooserWithMemory(name="Memory chooser")
    tree = create_tree(chooser, "fail-after-one")
    tick_four_times(tree)
    assert(tree.status == py_trees.common.Status.SUCCESS)

    chooser = py_trees.composites.ChooserWithMemory(name="Memory chooser")
    tree = create_tree(chooser, "fail-after-one-then-immediate")
    tick_four_times(tree)
    assert(tree.status == py_trees.common.Status.SUCCESS)

def test_chooser_default():
    console.banner("Default Chooser")

    chooser = py_trees.composites.Chooser(name="Default chooser")
    tree = create_tree(chooser, "immediate-failure")
    tick_four_times(tree)
    assert(tree.status == py_trees.common.Status.SUCCESS)

    chooser = py_trees.composites.Chooser(name="Default chooser")
    tree = create_tree(chooser, "fail-after-one")
    tick_four_times(tree)
    assert(tree.status == py_trees.common.Status.FAILURE)

    chooser = py_trees.composites.Chooser(name="Default chooser")
    tree = create_tree(chooser, "fail-after-one-then-immediate")
    tick_four_times(tree)
    assert(tree.status == py_trees.common.Status.SUCCESS)


##############################################################################
# Helper functions
##############################################################################


def tick_four_times(tree):
    for i in range(1,5):
        print("\n--------- Tick {0} ---------\n".format(i))
        tree.tick_once()
        print("\n")
        print(py_trees.display.ascii_tree(tree, show_status=True))


class FailAfterOne(py_trees.behaviour.Behaviour):
    def __init__(self, name="Counter"):
        super(FailAfterOne, self).__init__(name)

    def initialise(self):
        self.counter = 0

    def update(self):
        self.counter += 1
        if self.counter == 1:
            return py_trees.common.Status.RUNNING
        else:
            return py_trees.common.Status.FAILURE


class FailAfterOneThenImmediate(py_trees.behaviour.Behaviour):
    def __init__(self, name="Counter"):
        super(FailAfterOneThenImmediate, self).__init__(name)
        self.counter = 0

    def update(self):
        self.counter += 1
        if self.counter == 1:
            return py_trees.common.Status.RUNNING
        else:
            return py_trees.common.Status.FAILURE


def create_tree(chooser, scenario):
    root = chooser
    success = py_trees.behaviours.Success(name="Success")
    if scenario == "immediate-failure":
        root.add_child(py_trees.behaviours.Failure(name="Failure"))
    elif scenario == "fail-after-one":
        root.add_child(FailAfterOne("FailAfterOne"))
    elif scenario == "fail-after-one-then-immediate":
        root.add_child(FailAfterOneThenImmediate(name="FailAfterOneThenImmediate"))
    root.add_child(success)
    return root

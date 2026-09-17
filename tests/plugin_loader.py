"""Loading the plugin from a checkout.

``easyenv_workspaces/`` is the plugin, the directory sshPilot copies into its
plugins folder, so there is no installed package to import. The modules
that stand alone are loaded by path; the whole plugin is loaded as a package
under a name of its own, the way sshPilot's loader does it.
"""

import importlib.util
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(REPO, "easyenv_workspaces")
PACKAGE = "sshpilot_easyenv_under_test"


def load(name):
    """A module that imports nothing from its siblings."""
    spec = importlib.util.spec_from_file_location(
        f"easyenv_{name}", os.path.join(ROOT, f"{name}.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_plugin():
    """The whole plugin, relative imports and all. Needs sshPilot."""
    if PACKAGE in sys.modules:
        return sys.modules[PACKAGE]
    spec = importlib.util.spec_from_file_location(
        PACKAGE, os.path.join(ROOT, "__init__.py"), submodule_search_locations=[ROOT])
    module = importlib.util.module_from_spec(spec)
    sys.modules[PACKAGE] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        del sys.modules[PACKAGE]
        raise
    return module

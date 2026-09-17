import json
import os

from plugin_loader import REPO, ROOT


def manifest():
    with open(os.path.join(ROOT, "plugin.json"), encoding="utf-8") as fh:
        return json.load(fh)


def test_the_id_is_the_published_one_so_it_updates_in_place():
    assert manifest()["id"] == "easyenv-workspaces"


def test_the_manifest_asks_for_what_the_code_uses():
    m = manifest()
    assert m["api_version"] == 1
    assert m["entry"] == "plugin"
    # process: ssh runs the proxy; filesystem: the easyenv CLI's config file.
    assert set(m["permissions"]) >= {"network", "connections", "ui", "process", "filesystem"}


def test_every_module_the_plugin_imports_is_shipped():
    for name in ("__init__", "easyenv_api", "model", "connections", "page", "dialogs", "cli_config", "logos"):
        assert os.path.isfile(os.path.join(ROOT, f"{name}.py")), name


def test_the_package_script_ships_the_same_modules():
    with open(os.path.join(REPO, "scripts", "package.sh"), encoding="utf-8") as fh:
        script = fh.read()
    for name in ("__init__.py", "easyenv_api.py", "model.py", "connections.py",
                 "page.py", "dialogs.py", "cli_config.py", "logos.py", "plugin.json"):
        assert name in script, name

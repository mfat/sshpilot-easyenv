import json, os
HERE = os.path.dirname(__file__)

def test_manifest_valid():
    m = json.load(open(os.path.join(HERE, "..", "plugin.json")))
    assert m["id"] == "easyenv-workspaces"
    assert m["api_version"] == 1
    assert isinstance(m.get("permissions"), list)

def test_has_entry_module():
    assert os.path.isfile(os.path.join(HERE, "..", "__init__.py"))

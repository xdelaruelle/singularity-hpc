#!/usr/bin/python

# Copyright (C) 2021 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import shutil
import os
import io

from shpc.main import get_client

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)


def init_client(tmpdir, module_sys):
    """Get a common client for singularity and lmod"""
    settings_file = os.path.join(root, "settings.yml")
    new_settings = os.path.join(tmpdir, "settings.yml")
    shutil.copyfile(settings_file, new_settings)
    client = get_client(
        quiet=False,
        settings_file=new_settings,
        module=module_sys,
        container_tech="singularity",
    )

    # The module folder needs to be temporary too
    modules = os.path.join(tmpdir, "modules")
    modules = os.path.join(tmpdir, "containers")
    client.settings.set("module_base", modules)
    client.settings.set("container_base", modules)
    client.settings.save()
    return client


@pytest.mark.parametrize(
    "module_sys,module_file", [("lmod", "module.lua"), ("tcl", "module.tcl")]
)
def test_install_get(tmp_path, module_sys, module_file):
    """Test install and get"""
    client = init_client(str(tmp_path), module_sys)

    # Install known tag
    client.install("python:3.9.2-alpine")

    # Modules folder is created
    assert os.path.exists(client.settings.module_base)

    module_dir = os.path.join(client.settings.module_base, "python", "3.9.2-alpine")
    assert os.path.exists(module_dir)
    module_file = os.path.join(module_dir, module_file)
    assert os.path.exists(module_file)

    assert client.get("python/3.9.2-alpine")


@pytest.mark.parametrize("module_sys", [("lmod"), ("tcl")])
def test_docgen(tmp_path, module_sys):
    """Test docgen"""
    client = init_client(str(tmp_path), module_sys)
    client.install("python:3.9.2-slim")
    out = io.StringIO()
    docs = client.docgen("python:3.9.2-slim", out)
    docs = docs.getvalue()
    assert "python:3.9.2-slim" in docs


@pytest.mark.parametrize("module_sys", [("lmod"), ("tcl")])
def test_inspect(tmp_path, module_sys):
    """Test inspect"""
    client = init_client(str(tmp_path), module_sys)
    client.install("python:3.9.2-slim")

    # Install known registry item latest
    with pytest.raises(SystemExit):
        client.inspect("python")

    # Python won't have much TODO we should test a custom container
    metadata = client.inspect("python/3.9.2-slim")
    assert "attributes" in metadata


@pytest.mark.parametrize("module_sys", [("lmod"), ("tcl")])
def test_namespace_and_show(tmp_path, module_sys):
    """Test namespace and show"""
    client = init_client(str(tmp_path), module_sys)
    client.show("vanessa/salad:latest")

    with pytest.raises(SystemExit):
        client.show("salad:latest")
    client.settings.set("namespace", "vanessa")
    client.show("salad:latest")
    client.settings.set("namespace", None)


@pytest.mark.parametrize("module_sys", [("lmod"), ("tcl")])
def test_check(tmp_path, module_sys):
    """Test check"""
    client = init_client(str(tmp_path), module_sys)
    client.install("python:3.9.2-slim")

    # Python won't have much TODO we should test a custom container
    client.check("python/3.9.2-slim")


@pytest.mark.parametrize("module_sys", [("lmod"), ("tcl")])
def test_add(tmp_path, module_sys):
    """Test adding a custom container"""
    client = init_client(str(tmp_path), module_sys)

    # Create a copy of the latest image to add
    container = os.path.join(str(tmp_path), "salad_latest.sif")
    shutil.copyfile(os.path.join(here, "testdata", "salad_latest.sif"), container)
    client.add(container, "dinosaur/salad/latest")
    assert client.get("dinosaur/salad/latest")

from .toctree import SubprojectTocTree
from urllib.parse import urlparse
import os
import sys
from pathlib import Path
from sphinx.addnodes import toctree as ToctreeNode
import requests
import socket
import logging
from .utils import get_normalized_master_url, is_subproject

logger = logging.getLogger(__name__)


def add_master_toctree_to_index(app, doctree):
    if not is_subproject(app.config):
        return
    curr_docname = app.env.docname
    if Path(doctree.attributes["source"]).name == "master__.rst":
        # When parsing the master file, save the entries
        # We parse this file first, so self.env.master_entries is always set
        # when parsing the other docs
        toctrees = list(doctree.document.findall(ToctreeNode))
        if len(toctrees) != 1:
            logger.error("Expecting only one toctree in master project index.")
            sys.exit(1)
        toctree = toctrees[0]
        app.env.master_entries = toctree.attributes["entries"]
    elif curr_docname == "index":
        # Insert entries from master doc into subproject index as urls
        assert app.env.master_entries
        subproject_name = os.getenv("READTHEDOCS_PROJECT")
        language = os.getenv("READTHEDOCS_LANGUAGE", default="en")
        version = os.getenv("READTHEDOCS_VERSION", default="latest")
        master_readthedocs_url = get_normalized_master_url(app.config)
        this_subproject_url = urlparse(
            f"{master_readthedocs_url}/projects/"
            f"{subproject_name}/"
            f"{language}/{version}/index.html"
        )
        toctrees = list(doctree.findall(ToctreeNode))
        if len(toctrees) > 1:
            logger.warning(
                "Found multiple toctrees in subproject index. "
                "Only adding master toctree entries to first toctree."
            )
        toctree = toctrees[0]
        new_entries = []
        for title, entry in app.env.master_entries:
            parsed_entry = urlparse(entry)
            if parsed_entry.netloc and parsed_entry.path == this_subproject_url.path:
                # To retain order from master index, only add subproject
                # index entries when the subproject is found in the master index
                new_entries.extend(toctree.attributes["entries"])
            else:
                # Master index entries are added as urls
                new_entry = (
                    f"{master_readthedocs_url}/{language}" f"/{version}/{entry}.html"
                )
                new_entries.append((title, new_entry))
        toctree.attributes["entries"] = new_entries
        env_toctree = list(app.env.tocs["index"].findall(ToctreeNode))[0]
        env_toctree["entries"] = new_entries


def read_master_first(app, env, docnames):
    if is_subproject(app.config):
        app.builder.read_doc("master__")
        if "master__" in docnames:
            docnames.remove("master__")
    (Path(app.srcdir) / "master__.rst").unlink(missing_ok=True)


def add_master_file(app, config):
    check_internet_connection()
    src_dir = Path(app.srcdir)
    if is_subproject(config):
        master_url = get_normalized_master_url(config)
        language = os.getenv("READTHEDOCS_LANGUAGE", default="en")
        version = os.getenv("READTHEDOCS_VERSION", default="latest")
        toctree_source_url = (
            f"{master_url}/{language}/" f"{version}/_sources/index.rst.txt"
        )
        response = requests.get(toctree_source_url)
        response.raise_for_status()
        data = response.text
        with (src_dir / "master__.rst").open("w") as open_masterdoc:
            open_masterdoc.write(data)


def check_internet_connection():
    try:
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        logger.error("Subprojecttoctree requires a working internet connection")
        sys.exit(1)


def remove_master(app, env):
    if is_subproject(app.config):
        env.found_docs.remove("master__")
        del env.all_docs["master__"]
        (Path(app.doctreedir) / "master__.doctree").unlink()


def always_read_index(app, env, added, changed, removed):
    return ["index"]


def setup(app):
    project_name = os.getenv("READTHEDOCS_PROJECT")
    if not project_name:
        logger.error(
            "Subprojecttoctree requires the environment variable "
            "'READTHEDOCS_PROJECT' to be set. Please define it "
            "when building the documentation locally."
        )
        sys.exit(1)
    app.add_config_value("readthedocs_url", None, "env", types=[str])
    app.add_config_value("is_subproject", None, "env", types=[bool])
    app.add_directive("subprojecttoctree", SubprojectTocTree)
    app.connect("env-get-outdated", always_read_index)
    app.connect("env-before-read-docs", read_master_first)
    app.connect("config-inited", add_master_file)
    app.connect("doctree-read", add_master_toctree_to_index)
    app.connect("env-updated", remove_master)
    return {
        "version": "0.1",
        "parallel_read_safe": False,
        "parallel_write_safe": True,
    }

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
from .builders import HTMLBuilder
from docutils import nodes

logger = logging.getLogger(__name__)


def find_first_toctree(doctree, is_root_index):
    toctrees = list(doctree.document.findall(ToctreeNode))
    if len(toctrees) > 1:
        if is_root_index:
            logger.error("Expecting only one toctree in master project index.")
            sys.exit(1)
        else:
            logger.warning(
                "Found multiple toctrees in subproject index. Only adding master toctree entries to first toctree."
            )
    toctree = toctrees[0]
    return toctree


def add_master_toctree_to_index(app, doctree):
    curr_docname = app.env.docname
    if curr_docname == "master__" or (
        not is_subproject(app.config) and curr_docname == "index"
    ):
        toctree = find_first_toctree(doctree, is_root_index=True)
        entries = toctree.attributes["entries"]
        app.env.master_entries = entries
        targets = [target for _, target in entries]
        toctree.attributes["includefiles"] = targets
        app.env.toctree_includes[curr_docname] = targets
    elif is_subproject(app.config) and curr_docname == "index":
        # Insert entries from master doc into subproject index as urls
        subproject_name = os.getenv("READTHEDOCS_PROJECT")
        language = os.getenv("READTHEDOCS_LANGUAGE", default="en")
        version = os.getenv("READTHEDOCS_VERSION", default="latest")
        master_readthedocs_url = get_normalized_master_url(app.config)
        this_subproject_url = urlparse(
            f"{master_readthedocs_url}/projects/"
            f"{subproject_name}/"
            f"{language}/{version}/index.html"
        )
        toctree = find_first_toctree(doctree, is_root_index=False)
        new_entries = []
        last_master_entry = None
        for title, entry in app.env.master_entries:
            parsed_entry = urlparse(entry)
            if parsed_entry.netloc and parsed_entry.path == this_subproject_url.path:
                # To retain order from master index, only add subproject
                # index entries when the subproject is found in the master index
                new_entries.extend(toctree.attributes["entries"])

                # also store the last master index entry,
                # so that we can use it to generate the previous
                if last_master_entry:
                    app.env.last_master_entry = last_master_entry
                    last_entry_title = nodes.title()
                    last_entry_title += nodes.Text(title)
                    app.env.titles[last_master_entry] = last_entry_title
            elif parsed_entry.scheme and parsed_entry.netloc:
                # Entry is a url, add as is.
                new_entries.append((title, entry))
            else:
                # Master index entries are added as urls
                new_entry = (
                    f"{master_readthedocs_url}/{language}/{version}/{entry}.html"
                )
                # TODO: Change to new_entries.append((entry, new_entry))
                new_entries.append((title, new_entry))
                toctree.attributes["includefiles"].append(new_entry)
                last_master_entry = new_entry
        toctree.attributes["entries"] = new_entries
        env_toctree = list(app.env.tocs["index"].findall(ToctreeNode))[0]
        env_toctree["entries"] = new_entries


def read_master_first(app, env, docnames):
    index_name = "master__" if is_subproject(app.config) else "index"
    app.builder.read_doc(index_name)
    if index_name in docnames:
        docnames.remove(index_name)
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
    app.add_builder(HTMLBuilder, override=True)
    return {
        "version": "0.1",
        "parallel_read_safe": False,
        "parallel_write_safe": True,
    }

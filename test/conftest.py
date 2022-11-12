import pytest
from sphinx.testing.path import path
from unittest import mock
import os
from textwrap import dedent
from functools import wraps
from sphinx.config import Config

try:
    import readthedocs_ext
except ImportError:
    readthedocs_ext = None


# Sphinx provides a lot of utilities to test extensions
# Load them here
pytest_plugins = ["sphinx.testing.fixtures", "pytester"]
collect_ignore = ["root"]


def pytest_configure(config):
    markers = [
        "disable_env: disable setting the READTHEDOCS_PROJECT environment variable."
        "do_not_patch_connection: do not patch socket.create_connection (it is patched by default in tests to skip internet availability check)."
    ]
    for marker in markers:
        config.addinivalue_line(
            "markers",
            marker,
        )


@pytest.fixture(scope="session")
def rootdir():
    return path(__file__).parent.abspath() / "roots"


@pytest.fixture(autouse=True)
def mock_settings_env_vars(request):
    env_vars_marker = request.node.get_closest_marker("disable_env")
    if not env_vars_marker:
        with mock.patch.dict(os.environ, {"READTHEDOCS_PROJECT": "foo"}):
            yield
    else:
        yield


@pytest.fixture()
def make_app(make_app):
    @wraps(make_app)
    def wrapper(*args, **kwargs):
        confoverwrites = kwargs.get("confoverrides", {})
        sphinx_config = Config.read(kwargs["srcdir"])
        new_extensions = sphinx_config.extensions
        if readthedocs_ext:
            new_extensions = ["readthedocs_ext.readthedocs"] + new_extensions
        confoverwrites["extensions"] = new_extensions
        kwargs["confoverrides"] = confoverwrites
        app_ = make_app(*args, **kwargs)
        return app_

    yield wrapper


@pytest.fixture
def non_html_format_builders():
    return ["latex", "text", "man", "texinfo", "texinfo", "xml"]


@pytest.fixture(autouse=True)
def mock_internet_connection(mocker, request):
    if "do_not_patch_connection" in request.keywords:
        return
    mocker.patch("socket.create_connection")


@pytest.fixture
def master_index(mocker):
    master_index = dedent(
        """\
                          Dolor sit
                          =========

                          .. subprojecttoctree::
                              amet
                              sed
                              test <subproject: foo>
                          """
    )
    mocked_response = mocker.Mock()
    mocked_response.text = master_index
    mocked_request = mocker.patch("requests.get")
    mocked_request.return_value = mocked_response
    return mocked_response

import pytest
from sphinx.testing.path import path
from unittest import mock
import os

# Sphinx provides a lot of utilities to test extensions
# Load them here
pytest_plugins = ['sphinx.testing.fixtures', 'pytester']
collect_ignore = ['root']

@pytest.fixture(scope='session')
def rootdir():
    return path(__file__).parent.abspath() / 'roots'


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(os.environ, {"READTHEDOCS_PROJECT": "foo"}):
        yield

@pytest.fixture
def non_html_format_builders():
    return ['latex', 'text', 'man', 'texinfo', 'texinfo', 'xml']
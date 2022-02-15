from sphinx.testing.util import assert_node
import pytest
from docutils.nodes import bullet_list
from sphinx.addnodes import toctree

@pytest.mark.sphinx('html', testroot='subprojecttoctree-master')
def test_process_doc(app):
    app.build()
    index_toctree = app.env.tocs['index']
    assert_node(index_toctree,
                [bullet_list, ([toctree])])
    assert_node(index_toctree[0], toctree, entries=[(None, 'foo'),
                                                    (None, 'bar'),
                                                    ("SubprojectTitle", 
                                                     "http://example/projects/lorem/en/latest/index.html")],
                                           includefiles=['foo', 'bar'])

    assert app.env.toc_num_entries['index'] == 0
    assert app.env.toctree_includes['index'] == ['foo', 'bar']
    assert app.env.files_to_rebuild['foo'] == {'index'}
    assert app.env.files_to_rebuild['bar'] == {'index'}
    assert app.env.glob_toctrees == set()
    assert app.env.numbered_toctrees == set()
    assert index_toctree[0]['entries'] == [(None, 'foo'),
                                           (None, 'bar'),
                                           ('SubprojectTitle',
                                            'http://example/projects/lorem/en/latest/index.html')]


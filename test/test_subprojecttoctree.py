from sphinx.testing.util import assert_node
import pytest
from docutils.nodes import bullet_list, list_item, reference
from sphinx.addnodes import toctree, compact_paragraph
from textwrap import dedent
import logging
from pathlib import Path


@pytest.mark.sphinx(
    "html",
    testroot="subprojecttoctree-master",
    confoverrides={"html_theme": "sphinx_rtd_theme"},
)
def test_build_master_doc(app):
    app.build()
    index_toctree = app.env.tocs["index"]
    assert_node(index_toctree, [bullet_list, ([toctree])])
    assert_node(
        index_toctree[0],
        toctree,
        entries=[
            (None, "foo"),
            (None, "bar"),
            ("SubprojectTitle", "http://example/projects/lorem/en/latest/index.html"),
        ],
        includefiles=["foo", "bar"],
    )

    assert app.env.toc_num_entries["index"] == 0
    assert app.env.toctree_includes["index"] == [
        "foo",
        "bar",
        "http://example/projects/lorem/en/latest/index.html",
    ]
    assert app.env.files_to_rebuild["foo"] == {"index"}
    assert app.env.files_to_rebuild["bar"] == {"index"}
    assert app.env.glob_toctrees == set()
    assert app.env.numbered_toctrees == set()
    assert index_toctree[0]["entries"] == [
        (None, "foo"),
        (None, "bar"),
        ("SubprojectTitle", "http://example/projects/lorem/en/latest/index.html"),
    ]


@pytest.mark.sphinx(
    "html",
    testroot="subprojecttoctree-master-with-regular-http-url",
    confoverrides={"html_theme": "sphinx_rtd_theme"},
)
def test_subproject_together_with_regular_link(app):
    app.build()
    index_toctree = app.env.tocs["index"]
    assert_node(index_toctree, [bullet_list, ([toctree])])
    assert_node(
        index_toctree[0],
        toctree,
        entries=[
            (None, "foo"),
            (None, "bar"),
            ("SubprojectTitle", "http://example/projects/lorem/en/latest/index.html"),
            ("example", "http://example.org/"),
        ],
        includefiles=["foo", "bar"],
    )

    assert app.env.toc_num_entries["index"] == 0
    assert app.env.toctree_includes["index"] == [
        "foo",
        "bar",
        "http://example/projects/lorem/en/latest/index.html",
        "http://example.org/",
    ]
    assert app.env.files_to_rebuild["foo"] == {"index"}
    assert app.env.files_to_rebuild["bar"] == {"index"}
    assert app.env.glob_toctrees == set()
    assert app.env.numbered_toctrees == set()
    assert index_toctree[0]["entries"] == [
        (None, "foo"),
        (None, "bar"),
        ("SubprojectTitle", "http://example/projects/lorem/en/latest/index.html"),
        ("example", "http://example.org/"),
    ]


@pytest.mark.sphinx(
    "html",
    testroot="subprojecttoctree-master-entry-after-subproject",
    confoverrides={"html_theme": "sphinx_rtd_theme"},
)
def test_build_master_doc_with_entry_after_subproject(app):
    app.build()
    index_toctree = app.env.tocs["index"]
    assert_node(index_toctree, [bullet_list, ([toctree])])
    assert_node(
        index_toctree[0],
        toctree,
        entries=[
            (None, "foo"),
            (None, "bar"),
            ("SubprojectTitle", "http://example/projects/lorem/en/latest/index.html"),
            (None, "ipsum"),
        ],
        includefiles=["foo", "bar", "ipsum"],
    )

    assert app.env.toc_num_entries["index"] == 0
    assert app.env.toctree_includes["index"] == [
        "foo",
        "bar",
        "http://example/projects/lorem/en/latest/index.html",
        "ipsum",
    ]
    assert app.env.files_to_rebuild["foo"] == {"index"}
    assert app.env.files_to_rebuild["bar"] == {"index"}
    assert app.env.files_to_rebuild["bar"] == {"index"}
    assert app.env.glob_toctrees == set()
    assert app.env.numbered_toctrees == set()
    assert index_toctree[0]["entries"] == [
        (None, "foo"),
        (None, "bar"),
        ("SubprojectTitle", "http://example/projects/lorem/en/latest/index.html"),
        (None, "ipsum"),
    ]


@pytest.mark.sphinx(
    "html",
    testroot="subprojecttoctree-subproject",
    confoverrides={"html_theme": "sphinx_rtd_theme"},
)
def test_build_subproject(master_index, app):
    app.build()
    assert app.env.toc_num_entries["index"] == 1
    assert app.env.toctree_includes["index"] == ["foo", "bar"]
    assert app.env.files_to_rebuild["foo"] == {"index"}
    assert app.env.files_to_rebuild["bar"] == {"index"}
    assert app.env.glob_toctrees == set()
    assert app.env.numbered_toctrees == set()

    index_toctree = app.env.tocs["index"]
    assert_node(
        index_toctree,
        [bullet_list, ([list_item, (compact_paragraph, [bullet_list, (toctree)])])],
    )
    assert_node(index_toctree[0][0], [compact_paragraph, reference, "Lorem Ipsum"])
    assert_node(index_toctree[0][0][0], reference, anchorname="")
    assert_node(
        index_toctree[0][1][0],
        toctree,
        caption=None,
        glob=False,
        hidden=False,
        includehidden=False,
        titlesonly=False,
        maxdepth=-1,
        entries=[
            (None, "http://example/en/latest/amet.html"),
            (None, "http://example/en/latest/sed.html"),
            (None, "foo"),
            (None, "bar"),
            ("explicit_ref", "http://example.org"),
        ],
        numbered=0,
        includefiles=[
            "foo",
            "bar",
            "http://example/en/latest/amet.html",
            "http://example/en/latest/sed.html",
        ],
        rawentries=["explicit_ref"],
    )


@pytest.mark.sphinx(
    "html",
    testroot="subprojecttoctree-subproject",
    confoverrides={"html_theme": "sphinx_rtd_theme"},
)
def test_build_subproject_multiple_master_toctrees(
    app_params, make_app, mocker, caplog
):
    master_index = dedent(
        """\
                          Dolor sit
                          =========

                          .. subprojecttoctree::
                              amet
                              sed
                              test <subproject: foo>

                          .. subprojecttoctree::
                              adipiscing
                              elit
                              test <subproject: foo>
                          """
    )
    mocked_response = mocker.Mock()
    mocked_response.text = master_index
    mocked_request = mocker.patch("requests.get")
    mocked_request.return_value = mocked_response
    args, kwargs = app_params
    app = make_app(*args, **kwargs)
    with pytest.raises(SystemExit):
        app.build()
    assert caplog.record_tuples == [
        (
            "subprojecttoctree",
            logging.ERROR,
            "Expecting only one toctree in master project index.",
        )
    ]


@pytest.mark.sphinx(
    "html",
    testroot="subprojecttoctree-subproject",
    confoverrides={"html_theme": "sphinx_rtd_theme"},
)
def test_build_subproject_entry_after_subproject(app_params, make_app, mocker):
    master_index = dedent(
        """\
                          Dolor sit
                          =========

                          .. subprojecttoctree::
                              amet
                              test <subproject: foo>
                              sed
                          """
    )
    mocked_response = mocker.Mock()
    mocked_response.text = master_index
    mocked_request = mocker.patch("requests.get")
    mocked_request.return_value = mocked_response
    args, kwargs = app_params
    app = make_app(*args, **kwargs)

    app.build()
    assert app.env.toc_num_entries["index"] == 1
    assert app.env.toctree_includes["index"] == ["foo", "bar"]
    assert app.env.files_to_rebuild["foo"] == {"index"}
    assert app.env.files_to_rebuild["bar"] == {"index"}
    assert app.env.glob_toctrees == set()
    assert app.env.numbered_toctrees == set()

    index_toctree = app.env.tocs["index"]
    assert_node(
        index_toctree,
        [bullet_list, ([list_item, (compact_paragraph, [bullet_list, (toctree)])])],
    )
    assert_node(index_toctree[0][0], [compact_paragraph, reference, "Lorem Ipsum"])
    assert_node(index_toctree[0][0][0], reference, anchorname="")
    assert_node(
        index_toctree[0][1][0],
        toctree,
        caption=None,
        glob=False,
        hidden=False,
        includehidden=False,
        titlesonly=False,
        maxdepth=-1,
        entries=[
            (None, "http://example/en/latest/amet.html"),
            (None, "foo"),
            (None, "bar"),
            ("explicit_ref", "http://example.org"),
            (None, "http://example/en/latest/sed.html"),
        ],
        numbered=0,
        includefiles=[
            "foo",
            "bar",
            "http://example/en/latest/amet.html",
            "http://example/en/latest/sed.html",
        ],
        rawentries=["explicit_ref"],
    )


@pytest.mark.sphinx(
    "html",
    testroot="subprojecttoctree-subproject",
    confoverrides={"html_theme": "sphinx_rtd_theme"},
)
def test_build_subproject_multiple_master_subprojects(app_params, make_app, mocker):
    master_index = dedent(
        """\
                          Dolor sit
                          =========

                          .. subprojecttoctree::
                              amet
                              test <subproject: foo>
                              sed
                              subproject2 <subproject: bar>
                          """
    )
    mocked_response = mocker.Mock()
    mocked_response.text = master_index
    mocked_request = mocker.patch("requests.get")
    mocked_request.return_value = mocked_response
    args, kwargs = app_params
    app = make_app(*args, **kwargs)

    app.build()
    assert app.env.toc_num_entries["index"] == 1
    assert app.env.toctree_includes["index"] == ["foo", "bar"]
    assert app.env.files_to_rebuild["foo"] == {"index"}
    assert app.env.files_to_rebuild["bar"] == {"index"}
    assert app.env.glob_toctrees == set()
    assert app.env.numbered_toctrees == set()

    index_toctree = app.env.tocs["index"]
    assert_node(
        index_toctree,
        [bullet_list, ([list_item, (compact_paragraph, [bullet_list, (toctree)])])],
    )
    assert_node(index_toctree[0][0], [compact_paragraph, reference, "Lorem Ipsum"])
    assert_node(index_toctree[0][0][0], reference, anchorname="")
    assert_node(
        index_toctree[0][1][0],
        toctree,
        caption=None,
        glob=False,
        hidden=False,
        includehidden=False,
        titlesonly=False,
        maxdepth=-1,
        entries=[
            (None, "http://example/en/latest/amet.html"),
            (None, "foo"),
            (None, "bar"),
            ("explicit_ref", "http://example.org"),
            (None, "http://example/en/latest/sed.html"),
            ("subproject2", "http://example/projects/bar/en/latest/index.html"),
        ],
        numbered=0,
        includefiles=[
            "foo",
            "bar",
            "http://example/en/latest/amet.html",
            "http://example/en/latest/sed.html",
        ],
        rawentries=["explicit_ref"],
    )


@pytest.mark.sphinx(
    "html",
    testroot="subprojecttoctree-subproject-multiple-toctrees",
    confoverrides={"html_theme": "sphinx_rtd_theme"},
)
def test_build_subproject_multiple_subproject_toctrees(master_index, app, caplog):
    app.build()
    assert caplog.record_tuples == [
        (
            "subprojecttoctree",
            logging.WARNING,
            "Found multiple toctrees in subproject index. "
            "Only adding master toctree entries to first toctree.",
        )
    ]


@pytest.mark.sphinx(
    "html",
    testroot="subprojecttoctree-subproject",
    confoverrides={"html_theme": "sphinx_rtd_theme"},
)
def test_build_subproject_master_already_present(master_index, app_params, make_app):
    _, kwargs = app_params
    existing_master_file = Path(kwargs["srcdir"] / "master__.rst")
    existing_master_file.touch()
    args, kwargs = app_params
    app = make_app(*args, **kwargs)
    app.build()
    assert not existing_master_file.exists()


@pytest.mark.sphinx(
    "html",
    testroot="subprojecttoctree-subproject-nested",
    confoverrides={"html_theme": "sphinx_rtd_theme"},
)
def test_build_subproject_nested_raises(master_index, app_params, make_app, caplog):
    args, kwargs = app_params
    app = make_app(*args, **kwargs)
    with pytest.raises(SystemExit):
        app.build()
    assert caplog.record_tuples == [
        (
            "subprojecttoctree.toctree",
            logging.ERROR,
            "Nested subprojects are not allowed. "
            "Either tag this project as the master by using 'is_subproject=False',"
            "or remove the subproject entry from the index.",
        )
    ]


@pytest.mark.sphinx(
    "html",
    testroot="subprojecttoctree-subproject",
    confoverrides={"html_theme": "sphinx_rtd_theme"},
)
def test_build_subproject_url_not_set(master_index, app_params, make_app, caplog):
    args, kwargs = app_params
    app = make_app(*args, **kwargs)
    app.config.readthedocs_url = None
    with pytest.raises(SystemExit):
        app.build()
    assert caplog.record_tuples == [
        (
            "subprojecttoctree.utils",
            logging.ERROR,
            "The 'readthedocs_url' config value must be set.",
        )
    ]


@pytest.mark.sphinx(
    "html",
    testroot="subprojecttoctree-subproject",
    confoverrides={"html_theme": "sphinx_rtd_theme"},
)
def test_build_subproject_is_subproject_not_set(
    master_index, app_params, make_app, caplog
):
    args, kwargs = app_params
    app = make_app(*args, **kwargs)
    app.config.is_subproject = None
    with pytest.raises(SystemExit):
        app.build()
    assert caplog.record_tuples == [
        (
            "subprojecttoctree.utils",
            logging.ERROR,
            "The 'is_subproject' config value must be set.",
        )
    ]


@pytest.mark.sphinx(
    "html",
    testroot="subprojecttoctree-subproject",
    confoverrides={"html_theme": "sphinx_rtd_theme"},
)
def test_build_subproject_url_wrong_protocol(
    master_index, app_params, make_app, caplog
):
    args, kwargs = app_params
    app = make_app(*args, **kwargs)
    app.config.readthedocs_url = "ftp://example.org"
    with pytest.raises(SystemExit):
        app.build()
    assert caplog.record_tuples == [
        (
            "subprojecttoctree.utils",
            logging.ERROR,
            "The 'readthedocs_url' config value must be eihter a 'http' or 'https' url.",
        )
    ]


@pytest.mark.sphinx(
    "html",
    testroot="subprojecttoctree-subproject",
    confoverrides={"html_theme": "sphinx_rtd_theme"},
)
def test_build_subproject_url_wrong_netloc(master_index, app_params, make_app, caplog):
    args, kwargs = app_params
    app = make_app(*args, **kwargs)
    app.config.readthedocs_url = "http://"
    with pytest.raises(SystemExit):
        app.build()
    assert caplog.record_tuples == [
        (
            "subprojecttoctree.utils",
            logging.ERROR,
            'The url specified in the config for "readthedocs_url" is invalid.',
        )
    ]


@pytest.mark.sphinx(
    "html",
    testroot="subprojecttoctree-subproject",
    confoverrides={"html_theme": "sphinx_rtd_theme"},
)
def test_build_subproject_wrong_subproject_format(app_params, make_app, mocker, caplog):
    master_index = dedent(
        """\
                          Dolor sit
                          =========

                          .. subprojecttoctree::
                              amet
                              sed
                              test <subproject:  >
                          """
    )
    mocked_response = mocker.Mock()
    mocked_response.text = master_index
    mocked_request = mocker.patch("requests.get")
    mocked_request.return_value = mocked_response
    args, kwargs = app_params
    app = make_app(*args, **kwargs)
    app.build()
    assert caplog.record_tuples == [
        (
            "subprojecttoctree.toctree",
            logging.WARNING,
            'No subproject name found after "subproject:" tag.',
        )
    ]


@pytest.mark.do_not_patch_connection
@pytest.mark.sphinx(
    "html",
    testroot="subprojecttoctree-subproject",
    confoverrides={"html_theme": "sphinx_rtd_theme"},
)
def test_build_no_working_internet_connection(app_params, make_app, mocker, caplog):
    mocked_connection = mocker.patch("socket.create_connection")
    mocked_connection.side_effect = OSError("Mocked connection")
    args, kwargs = app_params
    with pytest.raises(SystemExit):
        make_app(*args, **kwargs)
    assert caplog.record_tuples == [
        (
            "subprojecttoctree",
            logging.ERROR,
            "Subprojecttoctree requires a working internet connection",
        )
    ]


@pytest.mark.disable_env
@pytest.mark.sphinx(
    "html",
    testroot="subprojecttoctree-subproject",
    confoverrides={"html_theme": "sphinx_rtd_theme"},
)
def test_no_env_variable_set(app_params, make_app, caplog):
    args, kwargs = app_params
    with pytest.raises(SystemExit):
        make_app(*args, **kwargs)
    assert caplog.record_tuples == [
        (
            "subprojecttoctree",
            logging.ERROR,
            "Subprojecttoctree requires the environment variable "
            "'READTHEDOCS_PROJECT' to be set. Please define it "
            "when building the documentation locally.",
        )
    ]


@pytest.mark.sphinx(
    "html",
    testroot="subprojecttoctree-subproject",
    confoverrides={"html_theme": "sphinx_rtd_theme"},
)
def test_build_subproject_root_index_next_previous_links(master_index, app):
    app.builder.build_all()
    result = (app.outdir / "index.html").read_text(encoding="utf8")

    # Check if the index html contains a 'previous' button
    # that navigates to the last entry from the master project
    assert (
        '<a href="http://example/en/latest/sed.html" class="btn btn-neutral float-left" title="test" accesskey="p" rel="prev"><span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous</a>'
        in result
    )

    # Forward button should be a relative link to the next page
    assert (
        '<a href="foo.html" class="btn btn-neutral float-right" title="foo" accesskey="n" rel="next">Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span></a>'
        in result
    )


@pytest.mark.sphinx(
    "html",
    testroot="subprojecttoctree-subproject",
    confoverrides={"html_theme": "sphinx_rtd_theme"},
)
def test_subproject_root_index_next_previous_links(master_index, app):
    app.builder.build_all()
    result = (app.outdir / "index.html").read_text(encoding="utf8")

    # Check if the index html contains a 'previous' button
    # that navigates to the last entry from the master project
    assert (
        '<a href="http://example/en/latest/sed.html" class="btn btn-neutral float-left" title="test" accesskey="p" rel="prev"><span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous</a>'
        in result
    )

    # Forward button should be a relative link to the next page
    assert (
        '<a href="foo.html" class="btn btn-neutral float-right" title="foo" accesskey="n" rel="next">Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span></a>'
        in result
    )


@pytest.mark.sphinx(
    "html",
    testroot="subprojecttoctree-master",
    confoverrides={"html_theme": "sphinx_rtd_theme"},
)
def test_master_project_next_previous_links(app):
    app.builder.build_all()
    result = (app.outdir / "bar.html").read_text(encoding="utf8")

    # Check if html containt a forward button to the first entry of the subproject
    assert (
        '<a href="http://example/projects/lorem/en/latest/index.html" class="btn btn-neutral float-right" title="SubprojectTitle" accesskey="n" rel="next">Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span></a>'
        in result
    )

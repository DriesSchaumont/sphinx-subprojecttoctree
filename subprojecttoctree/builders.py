from __future__ import annotations
from .utils import is_subproject, get_normalized_master_url
from sphinx.builders.html import StandaloneHTMLBuilder


class HTMLBuilder(StandaloneHTMLBuilder):
    def prepare_writing(self, docnames) -> None:
        super().prepare_writing(docnames)
        if is_subproject(self.config):
            last_master_entry = self.env.last_master_entry
            self.relations[last_master_entry] = [None, None, "index"]
            self.relations["index"] = [
                last_master_entry,
                last_master_entry,
                self.relations["index"][2],
            ]

    def get_relative_uri(self, from_: str, to: str, typ: str = None) -> str:
        master_url = get_normalized_master_url(self.config)
        if to.startswith(master_url):
            return to
        return super().get_relative_uri(from_, to, typ)

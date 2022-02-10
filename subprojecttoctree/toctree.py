
import os
from sphinx.directives.other import TocTree

from sphinx import addnodes
from typing import List
from docutils.nodes import Node
from sphinx.util.nodes import explicit_title_re
from sphinx.util import logging
import re
from copy import deepcopy
from .utils import get_normalized_master_url, is_subproject

logger = logging.getLogger(__name__)

subproject_re = re.compile(r"""^\s?subproject:(.+)""")

class SubprojectTocTree(TocTree):
    def parse_content(self, toctree: addnodes.toctree) -> List[Node]:
        master_readthedocs_url = get_normalized_master_url(self.config)
        language = os.getenv('READTHEDOCS_LANGUAGE', default='en')
        version = os.getenv('READTHEDOCS_VERSION', default='latest')
        
        # First do some custom parsing ourselves, then for other options default to
        # default parser.
        to_add_later = {}
        removal_index_shift = 0 # Needed because self.content.remove(entry) does not work
        content_old = deepcopy(self.content)
        
        for i, entry in enumerate(self.content):
            if not entry:
                continue
            # Parse entries in the form 'title <ref>'
            explicit = explicit_title_re.match(entry)
            if explicit:
                ref = explicit.group(2)
                title = explicit.group(1)
                subproject = subproject_re.match(ref) # ref is 'subproject: ...'
                if subproject:
                    subproject_relative_path = subproject.group(1).strip()
                    if subproject_relative_path:
                        ref = (f"{master_readthedocs_url}/projects/{subproject_relative_path}"
                               f"/{language}/{version}/index.html")
                        to_add_later[i] = (title, ref)
                        # Remove from self.content, but not from the parents.
                        # So we do not use self.content.remove()
                        del self.content.data[i + removal_index_shift]
                        del self.content.items[i + removal_index_shift]
                        removal_index_shift -= 1
                    else:
                        logger.warning('No subproject name found after "subproject:" tag.')
        # We downloaded the 'master__' document, but it contains entries
        # which are not files in this source dir.
        # We presume that these entries reference existing html documents
        # which are hosted in the master project. So add them to 'found_docs'
        # Otherwise they would have been removed.
        orig_found_docs = self.env.found_docs.copy()
        if is_subproject(self.config) and toctree.attributes['parent'] == "master__":
            to_add = set(self.content) 
            self.env.found_docs.update(to_add)
        ret = super().parse_content(toctree)

        # Reset 'found docs'
        self.env.found_docs.clear()
        self.env.found_docs.update(orig_found_docs)

        # Add our own custom parsed entries to the toctree entries
        for i, to_add in to_add_later.items():
            toctree['entries'].insert(i, to_add)

        # Reset the content
        self.content = content_old
        return ret
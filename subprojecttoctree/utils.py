from urllib.parse import urlparse
import logging
import sys

logger = logging.getLogger(__name__)


def get_normalized_master_url(config):
    config_value = config.readthedocs_url
    if not config.readthedocs_url:
        logger.error("The 'readthedocs_url' config value must be set.")
        sys.exit(1)
    parsed_url = urlparse(config_value)
    if parsed_url.scheme not in ("http", "https"):
        logger.error(
            "The 'readthedocs_url' config value must be "
            "eihter a 'http' or 'https' url."
        )
        sys.exit(1)
    if not parsed_url.netloc:
        logger.error(
            'The url specified in the config for "readthedocs_url" is invalid.'
        )
        sys.exit(1)

    return f"{parsed_url.scheme}://{parsed_url.netloc.replace('/', '')}"


def is_subproject(config):
    flag = config.is_subproject
    if flag is None:
        logger.error("The 'is_subproject' config value must be set.")
        sys.exit(1)
    return flag

"""Module that contains the config parser."""

import yaml

from gmail_auto_forwarding.utils.schemas import ConfigFile

from .helpers import (
    verify_forward_filters_section,
    verify_forwarders_section,
    verify_proxies_section,
    verify_receiver_section,
    verify_script_section,
)


def parse_config(file_path: str) -> ConfigFile:
    """
    Parse the config file and return a ConfigFile object that contains the
    parsed config file.

    Refer to :class:`ConfigFile` for more information.

    Args:
        file_path: Path to the config file.

    Raises:
        ValueError: If the config file is invalid.

    Returns:
        A ConfigFile that contains the parsed config file.
    """

    with open(file_path, "r") as f:
        yaml_config = yaml.safe_load(f)

        receiver = verify_receiver_section(yaml_config.get("receiver", {}))

        forwarders = verify_forwarders_section(yaml_config.get("forwarders", []))

        forward_filters = verify_forward_filters_section(yaml_config.get("forward_filters", {}))

        script = verify_script_section(yaml_config.get("script", {}))

        proxies = verify_proxies_section(yaml_config.get("proxies", {}))

    return ConfigFile(receiver, forwarders, forward_filters, script, proxies)

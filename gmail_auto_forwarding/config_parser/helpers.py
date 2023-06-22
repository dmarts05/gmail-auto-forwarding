"""Module that contains helper functions for the config parser."""

from typing import Dict, List, Union


def verify_receiver_section(receiver: Dict[str, str]) -> Dict[str, str]:
    """
    Verify the receiver section of the config file.

    Args:
        receiver: The receiver section of the config file.

    Raises:
        ValueError: If the receiver section is invalid.

    Returns:
        The verified receiver section of the config file.
    """
    required_fields = ("email", "app_password")
    if not all(field in receiver for field in required_fields):
        raise ValueError("Missing required field(s) in receiver section of config file.")
    return receiver


def verify_forwarders_section(forwarders: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Verify the forwarders section of the config file.

    Args:
        forwarders: The forwarders section of the config file.

    Raises:
        ValueError: If the forwarders section is invalid.

    Returns:
        The verified forwarders section of the config file.
    """
    for forwarder in forwarders:
        required_fields = ("email", "password")
        if not all(field in forwarder for field in required_fields):
            raise ValueError("Missing required field(s) in forwarders section of config file.")
    return forwarders


def verify_forward_filters_section(
    forward_filters: Dict[str, Dict[str, List[str]]]
) -> Dict[str, Dict[str, List[str]]]:
    """
    Verify the forward filters section of the config file.

    Args:
        forward_filters: The forward filters section of the config file.

    Raises:
        ValueError: If the forward filters section is invalid.

    Returns:
        The verified forward filters section of the config file.
    """
    required_fields = (
        "from_emails",
        "to_emails",
        "subject",
        "has_words",
        "does_not_have_words",
        "has_attachments",
    )
    if not all(field in forward_filters for field in required_fields):
        raise ValueError("Missing required field(s) in forward filters section of config file.")
    return forward_filters


def verify_script_section(script: Dict[str, bool]) -> Dict[str, bool]:
    """
    Verify the script section of the config file.

    Args:
        script: The script section of the config file.

    Raises:
        ValueError: If the script section is invalid.

    Returns:
        The verified script section of the config file.
    """
    required_fields = ("headless", "virtual_display")
    if not all(field in script for field in required_fields):
        raise ValueError("Missing required field(s) in script section of config file.")
    return script


def verify_proxies_section(proxies: Union[Dict[str, bool], Dict[str, str]]) -> Union[Dict[str, bool], Dict[str, str]]:
    """
    Verify the Proxies section of the config file.

    Args:
        proxies: The Proxies section of the config file.

    Raises:
        ValueError: If the Proxies section is invalid.

    Returns:
        The verified Proxies section of the config file.
    """

    required_fields = ("enable", "list")
    if not all(field in proxies for field in required_fields):
        raise ValueError("Missing required field(s) in Proxies section of config file.")
    return proxies

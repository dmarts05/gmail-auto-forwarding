"""Module that contains the schemas used in the project."""

from typing import Dict, List, NamedTuple, Union


class ConfigFile(NamedTuple):
    """
    A schema that encapsulates the structure of the config file.

    receiver: the Gmail credentials of the receiver
        - email: the email address of the receiver
        - app_password: the app password of the receiver
    forwarders: a list of Gmail credentials of the forwarders
    forward_filters: the filter configuration for the emails that will be forwarded
        - from: a list of email addresses to filter
        - to: a list of email addresses to filter
        - subject: a list of keywords to filter
        - has_words: a list of keywords to filter
        - does_not_have_words: a list of keywords to filter
        - has_attachments: whether to filter emails with attachments
    script: the script configuration for Selenium
        - headless: whether to run the browser in headless mode
        - virtual_display: whether to run the browser in a virtual display
        - no_webdriver_manager: whether to use the webdriver manager
    proxies: the proxies configuration for Selenium
        - enable: whether to enable proxies
        - list: a list of proxies to use
    """

    receiver: Dict[str, str]
    forwarders: List[Dict[str, str]]
    forward_filters: Dict[str, Union[List[str], Dict[str, Union[int, bool]]]]
    script: Dict[str, bool]
    proxies: Union[Dict[str, str], Dict[str, bool]]

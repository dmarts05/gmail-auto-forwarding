"""Module for enabling auto-forwarding in Gmail."""

import random
from time import sleep
from typing import Dict, List

from selenium.webdriver.remote.webdriver import WebDriver

import gmail_auto_forwarding.forwarding_manager.constants as c
from gmail_auto_forwarding.utils.logger import setup_logger

from .helpers import (
    add_forward_filters,
    enable_forward_all_emails,
    enable_forwarding,
    login_to_gmail,
)

logger = setup_logger(logger_name=__name__)


def configure_forwarding(
    browser: WebDriver,
    forwarder: Dict[str, str],
    receiver: Dict[str, str],
    forward_filters: Dict[str, Dict[str, List[str]]],
) -> None:
    """
    Configure forwarding in Gmail for the given forwarder and receiver.

    Args:
        browser: Selenium browser that will be used to configure forwarding.
        forwarder: Dictionary containing the forwarder's email and password.
        receiver: Dictionary containing the receiver's email and app password.
        forward_filters: Dictionary containing the forward filters to be used.
    """
    logger.info("Logging in to Gmail...")
    login_to_gmail(browser, forwarder["email"], forwarder["password"])
    sleep(random.randint(c.WAIT_TIME_MIN, c.WAIT_TIME_MAX))

    logger.info("Enabling forwarding...")
    enable_forwarding(browser, receiver["email"], receiver["app_password"])
    sleep(random.randint(c.WAIT_TIME_MIN, c.WAIT_TIME_MAX))

    # Check if no forward filters were given, and if so, forward all emails
    if any(forward_filters.values()):
        logger.info("Forward filters were given, adding them...")
        add_forward_filters(browser, receiver["email"], forward_filters)
        sleep(random.randint(c.WAIT_TIME_MIN, c.WAIT_TIME_MAX))
    else:
        logger.info("No forwarding filters were given, enabling forwarding all emails...")
        enable_forward_all_emails(browser)
        sleep(random.randint(c.WAIT_TIME_MIN, c.WAIT_TIME_MAX))

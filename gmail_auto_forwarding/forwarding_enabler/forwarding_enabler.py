"""Module for enabling auto-forwarding in Gmail."""

import random
from time import sleep
from typing import Dict, List, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from gmail_auto_forwarding.browser.extra_actions import wait_for_element_until_clickable
from gmail_auto_forwarding.gmail_scraper.gmail_scraper import scrape_forwarding_code
from gmail_auto_forwarding.utils.logger import setup_logger

from .constants import (
    ADD_FORWARDING_ADDRESS_CSS_SELECTOR,
    CODE_INPUT_CSS_SELECTOR,
    EMAIL_INPUT_ID,
    EMAIL_NEXT_BUTTON_ID,
    FORWARDING_EMAIL_INPUT_CSS_SELECTOR,
    FORWARDING_NEXT_BUTTON_NAME,
    FORWARDING_SETTINGS_URL,
    GMAIL_URL,
    OK_BUTTON_NAME,
    PASSWORD_INPUT_NAME,
    PASSWORD_NEXT_BUTTON_ID,
    SUBMIT_BUTTON_CSS_SELECTOR,
    VERIFY_BUTTON_CSS_SELECTOR,
    WAIT_TIME_MAX,
    WAIT_TIME_MIN,
)

logger = setup_logger(logger_name=__name__)


def enable_forwarding(
    browser: WebDriver,
    forwarder: Dict[str, str],
    receiver: Dict[str, str],
    forward_filters: Dict[str, Union[List[str], Dict[str, Union[int, bool]]]],
) -> None:
    # Go to Gmail
    logger.info("Going to Gmail...")
    browser.get(GMAIL_URL)

    initial_window = browser.current_window_handle

    # Login to the forwarder's account
    logger.info("Logging in to the forwarder's account...")
    wait_for_element_until_clickable(browser, (By.ID, EMAIL_INPUT_ID)).send_keys(forwarder["email"])  # type: ignore
    browser.find_element(By.ID, EMAIL_NEXT_BUTTON_ID).click()
    wait_for_element_until_clickable(browser, (By.NAME, PASSWORD_INPUT_NAME)).send_keys(forwarder["password"])  # type: ignore # noqa: E501
    browser.find_element(By.ID, PASSWORD_NEXT_BUTTON_ID).click()
    sleep(random.randint(WAIT_TIME_MIN, WAIT_TIME_MAX))

    # Go to the forwarding settings
    logger.info("Going to the forwarding settings...")
    browser.get(FORWARDING_SETTINGS_URL)

    # TODO: Take into account sign in errors

    # Ask to enable forwarding
    logger.info("Asking to enable forwarding...")
    wait_for_element_until_clickable(browser, (By.CSS_SELECTOR, ADD_FORWARDING_ADDRESS_CSS_SELECTOR)).click()  # type: ignore # noqa: E501
    wait_for_element_until_clickable(browser, (By.CSS_SELECTOR, FORWARDING_EMAIL_INPUT_CSS_SELECTOR)).send_keys(receiver["email"])  # type: ignore # noqa: E501
    browser.find_element(By.NAME, FORWARDING_NEXT_BUTTON_NAME).click()
    sleep(random.randint(WAIT_TIME_MIN, WAIT_TIME_MAX))

    # Accept the confirmation dialog

    # Switch to the new window
    for window_handle in browser.window_handles:
        if window_handle != initial_window:
            browser.switch_to.window(window_handle)  # type: ignore
            break
    wait_for_element_until_clickable(browser, (By.CSS_SELECTOR, SUBMIT_BUTTON_CSS_SELECTOR)).click()

    # Switch back to the initial window
    browser.switch_to.window(initial_window)  # type: ignore

    # Accept the confirmation dialog (second one)
    wait_for_element_until_clickable(browser, (By.NAME, OK_BUTTON_NAME)).click()

    sleep(WAIT_TIME_MIN)

    # Get the forwarding code
    logger.info("Getting the forwarding code...")
    code = scrape_forwarding_code(receiver["email"], receiver["app_password"])
    logger.info(f"Forwarding code: {code}")

    # Write the forwarding code and verify forwarding address
    logger.info("Writing the forwarding code and verifying the forwarding address...")
    code_input = browser.find_element(By.CSS_SELECTOR, CODE_INPUT_CSS_SELECTOR)
    code_input.clear()
    code_input.send_keys(code)  # type: ignore

    browser.find_element(By.CSS_SELECTOR, VERIFY_BUTTON_CSS_SELECTOR).click()

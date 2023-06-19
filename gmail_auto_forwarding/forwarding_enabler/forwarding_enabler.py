"""Module for enabling auto-forwarding in Gmail."""

import random
from time import sleep
from typing import Dict, List, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from gmail_auto_forwarding.browser.extra_actions import wait_for_element_until_clickable

from .constants import (
    EMAIL_INPUT_ID,
    EMAIL_NEXT_BUTTON_ID,
    FORWARDING_EMAIL_INPUT_XPATH,
    FORWARDING_NEXT_BUTTON_NAME,
    FORWARDING_SETTINGS_URL,
    GMAIL_URL,
    OK_BUTTON_NAME,
    PASSWORD_INPUT_NAME,
    PASSWORD_NEXT_BUTTON_ID,
    SUBMIT_BUTTON_CSS_SELECTOR,
    WAIT_TIME_MAX,
    WAIT_TIME_MIN,
)


def enable_forwarding(
    browser: WebDriver,
    forwarder: Dict[str, str],
    receiver: Dict[str, str],
    forward_filters: Dict[str, Union[List[str], Dict[str, Union[int, bool]]]],
) -> None:
    # Go to Gmail
    browser.get(GMAIL_URL)

    initial_window = browser.current_window_handle

    # Login to the forwarder's account
    wait_for_element_until_clickable(browser, (By.ID, EMAIL_INPUT_ID)).send_keys(forwarder["email"])  # type: ignore
    browser.find_element(By.ID, EMAIL_NEXT_BUTTON_ID).click()
    wait_for_element_until_clickable(browser, (By.NAME, PASSWORD_INPUT_NAME)).send_keys(forwarder["password"])  # type: ignore # noqa: E501
    browser.find_element(By.ID, PASSWORD_NEXT_BUTTON_ID).click()
    sleep(random.randint(WAIT_TIME_MIN, WAIT_TIME_MAX))

    # Go to the forwarding settings
    browser.get(FORWARDING_SETTINGS_URL)

    # Ask to enable forwarding
    wait_for_element_until_clickable(browser, (By.XPATH, FORWARDING_EMAIL_INPUT_XPATH)).send_keys(receiver["email"])  # type: ignore # noqa: E501
    wait_for_element_until_clickable(browser, (By.CSS_SELECTOR, SUBMIT_BUTTON_CSS_SELECTOR)).click()
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

"""Module for enabling auto-forwarding in Gmail."""

import time
import random
from typing import Dict, List, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from gmail_auto_forwarding.browser.extra_actions import (
    wait_for_element_until_clickable,
    wait_for_element_until_visible,
)


def enable_forwarding(
    browser: WebDriver,
    forwarder: Dict[str, str],
    receiver: Dict[str, str],
    forward_filters: Dict[str, Union[List[str], Dict[str, Union[int, bool]]]],
) -> None:
    browser.get("https://www.gmail.com")

    initial_window = browser.current_window_handle

    wait_for_element_until_clickable(browser, (By.ID, "identifierId")).send_keys(forwarder["email"])  # type: ignore

    browser.find_element(By.ID, "identifierNext").click()

    wait_for_element_until_clickable(browser, (By.NAME, "Passwd")).send_keys(forwarder["password"])  # type: ignore

    browser.find_element(By.ID, "passwordNext").click()

    time.sleep(random.randint(2, 5))

    browser.get("https://mail.google.com/mail/u/0/#settings/fwdandpop")
    wait_for_element_until_visible(browser, (By.TAG_NAME, "body"))
    time.sleep(random.randint(2, 5))

    wait_for_element_until_clickable(browser, (By.XPATH, "/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div[6]/div/table/tbody/tr[1]/td[2]/div/div[2]/input")).click()  # type: ignore

    wait_for_element_until_clickable(browser, (By.CSS_SELECTOR, "div.PN > input")).send_keys(receiver["email"])  # type: ignore

    browser.find_element(By.NAME, "next").click()

    # Switch to the new window
    for window_handle in browser.window_handles:
        if window_handle != initial_window:
            browser.switch_to.window(window_handle)  # type: ignore
            break

    wait_for_element_until_clickable(browser, (By.CSS_SELECTOR, "input[type='submit']")).click()  # type: ignore

    # Switch back to the initial window
    browser.switch_to.window(initial_window)  # type: ignore

    wait_for_element_until_clickable(browser, (By.NAME, "ok")).click()

    time.sleep(30)

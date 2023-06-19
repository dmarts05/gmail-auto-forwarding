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

    wait_for_element_until_clickable(browser, (By.ID, "identifierId")).send_keys(forwarder["email"])  # type: ignore

    browser.find_element(By.ID, "identifierNext").click()

    wait_for_element_until_clickable(browser, (By.NAME, "Passwd")).send_keys(forwarder["password"])  # type: ignore

    browser.find_element(By.ID, "passwordNext").click()

    time.sleep(1)

    browser.get("https://mail.google.com/mail/u/0/#settings/fwdandpop")

    wait_for_element_until_clickable(browser, (By.XPATH, "/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div[6]/div/table/tbody/tr[1]/td[2]/div/div[2]/input")).click()  # type: ignore

    wait_for_element_until_clickable(browser, (By.ID, ":6r")).send_keys(receiver["email"])  # type: ignore

    browser.find_element(By.NAME, "next").click()

    time.sleep(10)

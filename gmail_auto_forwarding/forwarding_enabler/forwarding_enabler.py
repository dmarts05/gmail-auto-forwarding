"""Module for enabling auto-forwarding in Gmail."""

import random
from time import sleep
from typing import Dict, List, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

import gmail_auto_forwarding.forwarding_enabler.constants as c
from gmail_auto_forwarding.browser.extra_actions import wait_for_element_until_clickable
from gmail_auto_forwarding.gmail_scraper.gmail_scraper import scrape_forwarding_code
from gmail_auto_forwarding.utils.logger import setup_logger

logger = setup_logger(logger_name=__name__)


def enable_forwarding(
    browser: WebDriver,
    forwarder: Dict[str, str],
    receiver: Dict[str, str],
    forward_filters: Dict[str, Union[List[str], Dict[str, Union[int, bool]]]],
) -> None:
    # Go to Gmail
    logger.info("Going to Gmail...")
    browser.get(c.GMAIL_URL)

    initial_window = browser.current_window_handle

    # Login to the forwarder's account
    logger.info("Logging in to the forwarder's account...")
    wait_for_element_until_clickable(browser, (By.ID, c.EMAIL_INPUT_ID)).send_keys(forwarder["email"])  # type: ignore
    browser.find_element(By.ID, c.EMAIL_NEXT_BUTTON_ID).click()
    wait_for_element_until_clickable(browser, (By.NAME, c.PASSWORD_INPUT_NAME)).send_keys(forwarder["password"])  # type: ignore # noqa: E501
    browser.find_element(By.ID, c.PASSWORD_NEXT_BUTTON_ID).click()
    sleep(random.randint(c.WAIT_TIME_MIN, c.WAIT_TIME_MAX))

    # Go to the forwarding settings
    logger.info("Going to the forwarding settings...")
    browser.get(c.FORWARDING_SETTINGS_URL)

    # TODO: Take into account sign in errors

    # Ask to enable forwarding
    logger.info("Asking to enable forwarding...")
    wait_for_element_until_clickable(browser, (By.CSS_SELECTOR, c.ADD_FORWARDING_ADDRESS_CSS_SELECTOR)).click()  # type: ignore # noqa: E501
    wait_for_element_until_clickable(browser, (By.CSS_SELECTOR, c.FORWARDING_EMAIL_INPUT_CSS_SELECTOR)).send_keys(receiver["email"])  # type: ignore # noqa: E501
    browser.find_element(By.NAME, c.FORWARDING_NEXT_BUTTON_NAME).click()
    sleep(random.randint(c.WAIT_TIME_MIN, c.WAIT_TIME_MAX))

    # Accept the confirmation dialog

    # Switch to the new window
    for window_handle in browser.window_handles:
        if window_handle != initial_window:
            browser.switch_to.window(window_handle)  # type: ignore
            break
    wait_for_element_until_clickable(browser, (By.CSS_SELECTOR, c.SUBMIT_BUTTON_CSS_SELECTOR)).click()

    # Switch back to the initial window
    browser.switch_to.window(initial_window)  # type: ignore

    # Accept the confirmation dialog (second one)
    wait_for_element_until_clickable(browser, (By.NAME, c.OK_BUTTON_NAME)).click()

    sleep(c.WAIT_TIME_MIN)

    # Get the forwarding code
    logger.info("Getting the forwarding code...")
    code = scrape_forwarding_code(receiver["email"], receiver["app_password"])
    logger.info(f"Forwarding code: {code}")

    # Write the forwarding code and verify forwarding address
    logger.info("Writing the forwarding code and verifying the forwarding address...")
    code_input = browser.find_element(By.CSS_SELECTOR, c.CODE_INPUT_CSS_SELECTOR)
    code_input.clear()
    code_input.send_keys(code)  # type: ignore

    browser.find_element(By.CSS_SELECTOR, c.VERIFY_BUTTON_CSS_SELECTOR).click()
    sleep(random.randint(c.WAIT_TIME_MIN, c.WAIT_TIME_MAX))

    # Check if no forwarding filters were given, and if so, forward all emails
    if forward_filters:
        # Create forwarding filters
        logger.info("Creating forwarding filters...")
        # Phase 1
        browser.find_element(By.CSS_SELECTOR, c.CREATE_FILTER_1_BUTTON_CSS_SELECTOR).click()
        sleep(random.randint(c.WAIT_TIME_MIN, c.WAIT_TIME_MAX))

        if forward_filters["from_emails"]:
            from_emails_str = ",".join([f'"{email}"' for email in forward_filters["from_emails"]]).replace('"', "")
            browser.find_element(By.CSS_SELECTOR, c.FROM_INPUT_CSS_SELECTOR).send_keys(from_emails_str)  # type: ignore

        if forward_filters["to_emails"]:
            to_emails_str = ",".join([f'"{email}"' for email in forward_filters["to_emails"]]).replace('"', "")
            browser.find_element(By.CSS_SELECTOR, c.TO_INPUT_CSS_SELECTOR).send_keys(to_emails_str)  # type: ignore

        if forward_filters["subject"]:
            subject_str = ",".join([f'"{subject}"' for subject in forward_filters["subject"]]).replace('"', "")
            browser.find_element(By.CSS_SELECTOR, c.SUBJECT_INPUT_CSS_SELECTOR).send_keys(subject_str)  # type: ignore

        if forward_filters["has_words"]:
            has_words_str = ",".join([f'"{word}"' for word in forward_filters["has_words"]]).replace('"', "")
            browser.find_element(By.CSS_SELECTOR, c.HAS_WORDS_INPUT_CSS_SELECTOR).send_keys(has_words_str)  # type: ignore # noqa: E501

        if forward_filters["does_not_have_words"]:
            does_not_have_words_str = ",".join(
                [f'"{word}"' for word in forward_filters["does_not_have_words"]]
            ).replace('"', "")
            browser.find_element(By.CSS_SELECTOR, c.DOES_NOT_HAVE_WORDS_INPUT_CSS_SELECTOR).send_keys(does_not_have_words_str)  # type: ignore # noqa: E501

        if forward_filters["has_attachments"]:
            has_attachments_checkbox = browser.find_element(By.CSS_SELECTOR, c.HAS_ATTACHMENT_CHECKBOX_CSS_SELECTOR)
            browser.execute_script("arguments[0].checked = true;", has_attachments_checkbox)  # type: ignore

        # Phase 2
        browser.find_element(By.CSS_SELECTOR, c.CREATE_FILTER_2_BUTTON_CSS_SELECTOR).click()
        sleep(random.randint(c.WAIT_TIME_MIN, c.WAIT_TIME_MAX))

        forward_to_checkbox = browser.find_element(By.CSS_SELECTOR, c.FORWARD_TO_CHECKBOX_CSS_SELECTOR)
        browser.execute_script("arguments[0].checked = true;", forward_to_checkbox)  # type: ignore
        browser.find_element(By.CSS_SELECTOR, c.FORWARD_TO_SELECT_CSS_SELECTOR).click()
        browser.find_element(By.XPATH, c.FORWARD_TO_RECEIVER_OPTION_XPATH.format(receiver["email"])).click()

        # Phase 3
        browser.find_element(By.CSS_SELECTOR, c.CREATE_FILTER_3_BUTTON_CSS_SELECTOR).click()

        sleep(random.randint(c.WAIT_TIME_MIN, c.WAIT_TIME_MAX))
        logger.info("Forwarding filters created!")
    else:
        pass

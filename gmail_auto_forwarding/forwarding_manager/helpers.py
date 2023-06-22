"""Module containing helper functions for the forwarding manager."""

import random
from time import sleep
from typing import Dict, List

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

import gmail_auto_forwarding.forwarding_manager.constants as c
from gmail_auto_forwarding.browser.extra_actions import wait_for_element_until_clickable
from gmail_auto_forwarding.gmail_scraper.gmail_scraper import scrape_forwarding_code
from gmail_auto_forwarding.utils.exceptions import (
    DuplicateReceiverEmailException,
    FailedLoginException,
)
from gmail_auto_forwarding.utils.logger import setup_logger

logger = setup_logger(logger_name=__name__)


def login_to_gmail(browser: WebDriver, forwarder_email: str, forwarder_passwd: str) -> None:
    """
    Login to Gmail using the given email and password.

    Args:
        browser: Selenium browser that will be used to login to Gmail.
        forwarder_email: Email of the Gmail account to login to.
        forwarder_passwd: Password of the Gmail account to login to.
    Raises:
        FailedLoginException: If the login was unsuccessful.
    """
    logger.info(f"Logging in to {forwarder_email}...")
    browser.get(c.GMAIL_URL)

    # Enter email
    wait_for_element_until_clickable(browser, (By.ID, c.EMAIL_INPUT_ID)).send_keys(forwarder_email)  # type: ignore
    browser.find_element(By.ID, c.EMAIL_NEXT_BUTTON_ID).click()

    # Enter password
    wait_for_element_until_clickable(browser, (By.NAME, c.PASSWORD_INPUT_NAME)).send_keys(forwarder_passwd)  # type: ignore # noqa: E501
    browser.find_element(By.ID, c.PASSWORD_NEXT_BUTTON_ID).click()

    # Check if login was successful
    sleep(c.WAIT_TIME_MIN)
    browser.get(c.GMAIL_URL)
    logger.debug(f"Current URL: {browser.current_url}")
    if c.GMAIL_URL + "mail/u/" not in browser.current_url:
        raise FailedLoginException("Login failed! Your credentials are probably incorrect or you require 2FA.")

    logger.info("Login successful!")


def enable_forwarding(browser: WebDriver, receiver_email: str, receiver_app_passwd: str) -> None:
    """
    Enable forwarding in Gmail so that emails are forwarded to the given receiver email.

    Args:
        browser: Selenium browser that will be used to enable forwarding.
        receiver_email: Email of the receiver to forward emails to.
        receiver_app_passwd: App password of the receiver to check for the verification code.
    """
    logger.info("Going to forwarding settings...")
    browser.get(c.FORWARDING_SETTINGS_URL)

    # Store the initial window handle to switch back to it later
    initial_window = browser.current_window_handle

    logger.info(f"Adding forwarding address {receiver_email}...")
    wait_for_element_until_clickable(browser, (By.CSS_SELECTOR, c.ADD_FORWARDING_ADDRESS_CSS_SELECTOR)).click()
    wait_for_element_until_clickable(browser, (By.CSS_SELECTOR, c.FORWARDING_EMAIL_INPUT_CSS_SELECTOR)).send_keys(  # type: ignore # noqa: E501
        receiver_email
    )
    browser.find_element(By.NAME, c.FORWARDING_NEXT_BUTTON_NAME).click()
    sleep(random.randint(c.WAIT_TIME_MIN, c.WAIT_TIME_MAX))

    # Accept the confirmation dialog by switching to the new window
    for window_handle in browser.window_handles:
        if window_handle != initial_window:
            browser.switch_to.window(window_handle)  # type: ignore
            break
    try:
        wait_for_element_until_clickable(browser, (By.CSS_SELECTOR, c.SUBMIT_BUTTON_CSS_SELECTOR)).click()
    except TimeoutException:
        # Switch back to initial window
        browser.switch_to.window(initial_window)  # type: ignore
        raise DuplicateReceiverEmailException("Forwarding email address has been previously added!")

    # Switch back to initial window
    browser.switch_to.window(initial_window)  # type: ignore

    # Accept the second confirmation dialog
    wait_for_element_until_clickable(browser, (By.NAME, c.OK_BUTTON_NAME)).click()

    # Wait for the forwarding code to arrive in the receiver's inbox
    sleep(c.WAIT_TIME_MIN)

    # Get the forwarding code
    logger.info("Getting the forwarding code...")
    code = scrape_forwarding_code(receiver_email, receiver_app_passwd)

    # Write the forwarding code and verify forwarding address
    logger.info("Writing the forwarding code and verifying the forwarding address...")
    code_input = browser.find_element(By.CSS_SELECTOR, c.CODE_INPUT_CSS_SELECTOR)
    code_input.clear()
    code_input.send_keys(code)  # type: ignore

    browser.find_element(By.CSS_SELECTOR, c.VERIFY_BUTTON_CSS_SELECTOR).click()

    logger.info("Forwarding address successfully verified and enabled!")


def add_forward_filters(
    browser: WebDriver, receiver_email: str, forward_filters: Dict[str, Dict[str, List[str]]]
) -> None:
    """
    Add forward filters to the Gmail account.

    Args:
        browser: Selenium browser that will be used to add forward filters.
        receiver_email: Email of the receiver to forward emails to.
        forward_filters: Forward filters to add to the Gmail account.
    """
    logger.info("Adding forward filters...")

    # 1. Fill first filter form with the given filters
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
        browser.find_element(By.CSS_SELECTOR, c.HAS_WORDS_INPUT_CSS_SELECTOR).send_keys(has_words_str)  # type: ignore
    if forward_filters["does_not_have_words"]:
        does_not_have_words_str = ",".join([f'"{word}"' for word in forward_filters["does_not_have_words"]]).replace(
            '"', ""
        )
        browser.find_element(By.CSS_SELECTOR, c.DOES_NOT_HAVE_WORDS_INPUT_CSS_SELECTOR).send_keys(does_not_have_words_str)  # type: ignore # noqa: E501
    if forward_filters["has_attachments"]:
        has_attachments_checkbox = browser.find_element(By.CSS_SELECTOR, c.HAS_ATTACHMENT_CHECKBOX_CSS_SELECTOR)
        browser.execute_script("arguments[0].checked = true;", has_attachments_checkbox)  # type: ignore

    # 2. Fill second filter form enabling forwarding to the given receiver
    browser.find_element(By.CSS_SELECTOR, c.CREATE_FILTER_2_BUTTON_CSS_SELECTOR).click()
    sleep(random.randint(c.WAIT_TIME_MIN, c.WAIT_TIME_MAX))

    forward_to_checkbox = browser.find_element(By.CSS_SELECTOR, c.FORWARD_TO_CHECKBOX_CSS_SELECTOR)
    browser.execute_script("arguments[0].checked = true;", forward_to_checkbox)  # type: ignore
    browser.find_element(By.CSS_SELECTOR, c.FORWARD_TO_SELECT_CSS_SELECTOR).click()
    browser.find_element(By.XPATH, c.FORWARD_TO_RECEIVER_OPTION_XPATH.format(receiver_email)).click()

    # 3. Add filter
    browser.find_element(By.CSS_SELECTOR, c.CREATE_FILTER_3_BUTTON_CSS_SELECTOR).click()

    logger.info("Forward filters successfully added!")


def enable_forward_all_emails(browser: WebDriver) -> None:
    """
    Enable forwarding of all emails to the receiver.

    Args:
        browser: Selenium browser that will be used to enable forwarding of all emails.
    """
    browser.find_element(By.CSS_SELECTOR, c.FORWARD_COPY_RADIO_BUTTON_CSS_SELECTOR).click()
    browser.find_element(By.CSS_SELECTOR, c.SAVE_CHANGES_BUTTON_CSS_SELECTOR).click()
    logger.info("All emails will be forwarded!")

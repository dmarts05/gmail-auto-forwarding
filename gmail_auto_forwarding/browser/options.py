"""Module for getting browser options for Selenium."""

import platform
from typing import List

import requests
from undetected_chromedriver import ChromeOptions  # type: ignore

from gmail_auto_forwarding.utils.logger import setup_logger

from .proxies import get_random_working_proxy

logger = setup_logger(__name__)


def get_browser_language() -> str:
    """
    Get the user's browser language.

    Returns:
        The user's browser language
    """
    try:
        # Get the user's IP address
        response = requests.get("https://api.ipify.org?format=json")
        ip = response.json()["ip"]

        # Use the ipapi API to get the user's location data
        response = requests.get(f"https://ipapi.co/{ip}/json/")
        location_data = response.json()

        # Get the user's language preference
        lang = location_data["languages"].split(",")[0]
    except (requests.exceptions.RequestException, KeyError):
        # If the API request fails, default to English
        lang = "en-US"

    return lang


def get_chrome_browser_options(
    headless: bool = True, no_images: bool = True, proxies: List[str] = []
) -> ChromeOptions:
    """
    Returns a configured Chrome browser options instance.

    Args:
        headless: whether to run the browser in headless mode
        no_images: whether to disable images

    Returns:
        A Chrome browser options instance
    """
    options = ChromeOptions()
    # Add no images option if specified
    if no_images:
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # type: ignore
    # Add headless option if specified
    if headless:
        options.add_argument("--headless")  # type: ignore
    # Add proxies if specified
    if proxies:
        proxy = get_random_working_proxy(proxies)
        # Only add a proxy if a working one was found
        if proxy:
            logger.info(f"Using proxy {proxy}")
            options.add_argument(f"--proxy-server={proxy}")  # type: ignore
        else:
            logger.warning("No working proxies found, defaulting to no proxy")

    # Add options specific to Linux
    if platform.system() == "Linux":
        options.add_argument("--no-sandbox")  # type: ignore
        options.add_argument("--disable-dev-shm-usage")  # type: ignore

    return options

import os

from pyvirtualdisplay.display import Display

from gmail_auto_forwarding.browser.chrome import get_chrome_browser
from gmail_auto_forwarding.config_parser.config_parser import parse_config
from gmail_auto_forwarding.forwarding_enabler.forwarding_enabler import (
    enable_forwarding,
)
from gmail_auto_forwarding.utils.logger import reset_log_file, setup_logger

logger = setup_logger(logger_name=__name__)


def main() -> None:
    reset_log_file()

    logger.info("***********************************************")
    logger.info("*                                             *")
    logger.info("*           Gmail Auto Forwarding             *")
    logger.info("*                                             *")
    logger.info("***********************************************")

    # **************************************************************
    # Get program configuration
    # **************************************************************
    logger.info("Reading configuration file...")
    # Get path of config file in the parent directory
    config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config.yaml"))
    try:
        # Read config file
        config = parse_config(config_file_path)
    except ValueError as e:
        logger.error(str(e))
        exit(1)
    except FileNotFoundError:
        logger.error('Configuration file "config.yml" not found')
        exit(1)
    logger.info("Configuration file read successfully")
    logger.debug(f"Configuration: {config}")

    # **************************************************************
    # Get Selenium browser
    # **************************************************************
    # Start virtual display if enabled
    if config.script.get("virtual_display", False) and not config.script.get("headless", True):
        logger.info("Starting virtual display...")
        Display(visible=False, size=(1920, 1080)).start()
        logger.info("Virtual display started successfully")

    logger.info("Loading Selenium browser...")
    browser = get_chrome_browser(
        headless=config.script.get("headless", True),
        proxies=config.proxies.get("list", []) if config.proxies.get("enable", False) else [],  # type: ignore
    )
    logger.info("Selenium browser loaded successfully")

    # **************************************************************
    # Enable forwarding for each forwarder
    # **************************************************************
    for forwarder in config.forwarders:
        logger.info(f"Enabling forwarding for {forwarder['email']}...")
        enable_forwarding(browser, forwarder, config.receiver, config.forward_filters)


if __name__ == "__main__":
    main()

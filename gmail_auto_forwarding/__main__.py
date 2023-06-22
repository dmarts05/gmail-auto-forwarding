import json
import os

from pyvirtualdisplay.display import Display

from gmail_auto_forwarding.browser.chrome import get_chrome_browser
from gmail_auto_forwarding.config_parser.config_parser import parse_config
from gmail_auto_forwarding.forwarding_manager.forwarding_manager import (
    configure_forwarding,
)
from gmail_auto_forwarding.utils.exceptions import (
    DuplicateReceiverEmailException,
    FailedLoginException,
)
from gmail_auto_forwarding.utils.logger import reset_log_file, setup_logger
from gmail_auto_forwarding.utils.save_results import save_results

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
    CONFIG_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config.yaml"))
    try:
        # Read config file
        config = parse_config(CONFIG_FILE_PATH)
    except ValueError as e:
        logger.error(str(e))
        exit(1)
    except FileNotFoundError:
        logger.error('Configuration file "config.yml" not found')
        exit(1)
    logger.info("Configuration file read successfully")
    logger.debug(f"Configuration: {config}")

    # **************************************************************
    # Browser parameters
    # **************************************************************
    virtual_display = config.script.get("virtual_display", False)
    headless = config.script.get("headless", False)
    proxies = config.proxies.get("list", []) if config.proxies.get("enable", False) else []  # type: ignore

    # Start virtual display if enabled
    if virtual_display and not headless:
        logger.info("Starting virtual display...")
        Display(visible=False, size=(1920, 1080)).start()
        logger.info("Virtual display started successfully")

    # **************************************************************
    # Enable forwarding for each forwarder
    # **************************************************************
    results = {}
    for forwarder in config.forwarders:
        logger.info("Loading Selenium browser...")
        browser = get_chrome_browser(
            headless=headless,
            proxies=proxies,  # type: ignore
        )
        logger.info("Selenium browser loaded successfully")
        logger.info(f"Enabling forwarding for {forwarder['email']}...")
        try:
            configure_forwarding(browser, forwarder, config.receiver, config.forward_filters)
            results[forwarder["email"]] = "Success"
        except (FailedLoginException, DuplicateReceiverEmailException) as e:
            results[forwarder["email"]] = str(e)
            logger.error(str(e))
            logger.info("Continuing with next forwarder...")
        except Exception as e:
            results[forwarder["email"]] = "Unknown error"
            logger.error(e.__class__.__name__ + ": " + str(e))
            logger.info("Continuing with next forwarder...")
        finally:
            browser.quit()

    # **************************************************************
    # Print and save results
    # **************************************************************
    logger.info("Saving results...")
    RESULTS_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "results.txt"))
    save_results(results, RESULTS_FILE_PATH)
    logger.info("*** Results ***")
    logger.info(json.dumps(results, indent=4))


if __name__ == "__main__":
    main()

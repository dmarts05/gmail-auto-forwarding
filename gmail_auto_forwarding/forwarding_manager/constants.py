"""Module for storing constants used in the forwarding manager."""
# Wait time related constants
WAIT_TIME_MIN = 2
WAIT_TIME_MAX = 4

# URLs
GMAIL_URL = "https://www.gmail.com"
FORWARDING_SETTINGS_URL = "https://mail.google.com/mail/u/0/#settings/fwdandpop"

# Selectors for Gmail login
EMAIL_INPUT_ID = "identifierId"
EMAIL_NEXT_BUTTON_ID = "identifierNext"
PASSWORD_INPUT_NAME = "Passwd"
PASSWORD_NEXT_BUTTON_ID = "passwordNext"

# Selectors for adding a forwarding address
ADD_FORWARDING_ADDRESS_CSS_SELECTOR = "input[type=button]"
FORWARDING_EMAIL_INPUT_CSS_SELECTOR = "div.PN > input[type=text]"
FORWARDING_NEXT_BUTTON_NAME = "next"
SUBMIT_BUTTON_CSS_SELECTOR = "input[type='submit']"
OK_BUTTON_NAME = "ok"

CODE_INPUT_CSS_SELECTOR = "input[act=verifyText]"
VERIFY_BUTTON_CSS_SELECTOR = "input[act=verify]"

# Selectors for creating a forwarding filter
CREATE_FILTER_1_BUTTON_CSS_SELECTOR = "tbody span[role='link']"

FROM_INPUT_CSS_SELECTOR = "div.ZZ > div:nth-child(1) input"
TO_INPUT_CSS_SELECTOR = "div.ZZ > div:nth-child(2) input"
SUBJECT_INPUT_CSS_SELECTOR = "div.ZZ > div:nth-child(3) input"
HAS_WORDS_INPUT_CSS_SELECTOR = "div.ZZ > div:nth-child(4) input"
DOES_NOT_HAVE_WORDS_INPUT_CSS_SELECTOR = "div.ZZ > div:nth-child(5) input"
HAS_ATTACHMENT_CHECKBOX_CSS_SELECTOR = "div.ZZ input[type=checkbox]:nth-child(1)"
CREATE_FILTER_2_BUTTON_CSS_SELECTOR = "div.ZZ > div:nth-child(8) > div:nth-child(2)"

FORWARD_TO_CHECKBOX_CSS_SELECTOR = "div.ZZ > div:nth-child(3) > div > div:nth-child(5) input"
FORWARD_TO_SELECT_CSS_SELECTOR = "div.ZZ > div:nth-child(3) > div > div:nth-child(5) > span > div"
FORWARD_TO_RECEIVER_OPTION_XPATH = "//div[not(@role='option') and contains(text(), '{}')]"
CREATE_FILTER_3_BUTTON_CSS_SELECTOR = "div.ZZ > div:nth-child(4) > div"

# Selectors for forwarding all emails
FORWARD_COPY_RADIO_BUTTON_CSS_SELECTOR = "input[type=radio][value='1']"
SAVE_CHANGES_BUTTON_CSS_SELECTOR = "button[guidedhelpid='save_changes_button']"

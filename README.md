# Gmail Auto Forwarding
![Version](https://img.shields.io/badge/Version-1.0.0-brightgreen.svg)
![Python](https://img.shields.io/badge/Python-3.9-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

Gmail Auto Forwarding is a Python project that automatically enables forwarding between a receiver account and multiple forwarders using customizable filters for Gmail.

## Table of Contents
* [Features](#features)
* [Configuration](#configuration)
* [Installation with Poetry (recommended)](#installation-with-poetry-recommended)
* [Installation with pip](#installation-with-pip)
* [Development Setup](#development-setup)
* [Contributing](#contributing)
* [License](#license)

## Features
* Automatically enable forwarding.
* Multiple forwarders.
* Use filters to customize forwarding.
* Proxy support.

## Configuration
Before running the script, make sure to configure the necessary settings in the `config.yaml` file. You can use the provided `config.example.yaml` file as a template.

## Installation with Poetry (recommended)
To set up the project, follow these steps:
1. Make sure you have [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) installed in your system.
2. It is highly recommended to set this Poetry configuration parameter to avoid multiple issues:
    ```bash
    poetry config virtualenvs.in-project true
    poetry config virtualenvs.prefer-active-python true
    ```
3. Clone the repository:
    ```bash
    git clone https://github.com/dmarts05/gmail-auto-forwarding.git
    ```
4. Navigate to the project directory:
    ```bash
    cd gmail-auto-forwarding
    ```
5. Install the project dependencies using Poetry:
    ```bash
    poetry install
    ```
    You might need [pyenv](https://github.com/pyenv/pyenv) to install the Python version specified in the `pyproject.toml` file. If that's the case, run `pyenv install 3.9` before running the previous command. Also, check out the [Poetry documentation about pyenv](https://python-poetry.org/docs/managing-environments/) for more information.
6. Configure the script by updating the `config.yaml` file with your specific information (as mentioned in the previous section).
7. Run the script:
    ```bash
    poetry run gmail-auto-forwarding
    ```

## Installation with pip
This is an alternative installation method that uses pip instead of Poetry. It might not work as expected, so it is recommended to use the Poetry installation method instead. To set up the project, follow these steps:
1. Clone the repository:
    ```bash
    git clone https://github.com/dmarts05/gmail-auto-forwarding.git
    ```
2. Navigate to the project directory:
    ```bash
    cd gmail-auto-forwarding
    ```
3. Install the project dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```
    You might need [pyenv](https://github.com/pyenv/pyenv) to install the Python version specified in the `requirements.txt` file.
4. Configure the script by updating the `config.yaml` file with your specific information (as mentioned in the previous section).
5. Run the script:
    ```bash
    python -m gmail_auto_forwarding
    ```

## Development Setup
If you want to contribute to the project or run the development environment, follow these additional steps:
1. Install the development dependencies:
    ```bash
    poetry install --with dev
    ```
2. Install pre-commit hooks:
    ```bash
    poetry run pre-commit install
    ```
3. Format the code:
    ```bash
    poetry run black gmail_auto_forwarding
    ```
4. Lint the code:
    ```bash
    poetry run flake8 gmail_auto_forwarding
    ```
5. Run static type checking:
    ```bash
    poetry run mypy gmail_auto_forwarding
    ```
6. Generate the documentation:
    ```bash
    cd docs && poetry run make html
    ```
7. Do everything at once (except for generating the documentation):
    ```bash
    poetry run pre-commit run --all-files
    ```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/). See the [LICENSE](LICENSE) file for details.
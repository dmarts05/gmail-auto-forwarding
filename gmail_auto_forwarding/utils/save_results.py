import json
from typing import Dict


def save_results(results: Dict[str, str], file_path: str) -> None:
    """
    Save results to file.

    Args:
        results: Dictionary of results.
        file_path: Path to file to save results to.
    """
    try:
        with open(file_path, "w") as f:
            f.write(json.dumps(results, indent=4))
    except IOError:
        raise IOError("Could not save results to file")

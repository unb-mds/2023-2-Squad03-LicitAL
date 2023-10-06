import warnings
import sys

try:
    from ai_core_sdk.content.cli import cli
except (ImportError, ModuleNotFoundError):
    print(
        "The CLI is not available because dependencies are missing. "
        "Run 'pip install ai-core-sdk[aicore-content]' to install all "
        "dependencies needed."
    )
    sys.exit(1)
warnings.filterwarnings("ignore")

if __name__ == "__main__":
    cli()  # pylint: disable=E1120

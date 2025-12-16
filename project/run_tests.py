
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent / "tests"))

from tests.run_tests import main

if __name__ == "__main__":
    main()


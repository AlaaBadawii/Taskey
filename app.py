#!/usr/bin/env python3

from pathlib import Path
import sys


# Make the project importable as a package when this file is run directly.
PROJECT_ROOT = Path(__file__).resolve().parent
PACKAGE_NAME = PROJECT_ROOT.name
PARENT_DIR = str(PROJECT_ROOT.parent)

if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

package = __import__(PACKAGE_NAME, fromlist=["create_app"])
app = package.create_app()
db = package.db


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()

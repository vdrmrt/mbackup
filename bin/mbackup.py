#!/usr/bin/env python3
"""Compatibility wrapper for the package CLI."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mbackuplib.cli import main


if __name__ == '__main__':
    sys.exit(main())

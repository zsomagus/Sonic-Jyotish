#!/usr/bin/env python
"""Django admin parancssori interfész."""
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sonicjyotish.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Hiányzik a Django vagy rosszul van telepítve.") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

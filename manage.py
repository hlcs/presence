#!/usr/bin/env python
import os
import sys

"""Main del manage """
if __name__ == "__main__":
    """setta la variabile d' ambiente di django"""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "presence.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
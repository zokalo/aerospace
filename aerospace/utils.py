"""
Low-level utilities for ``aerospace`` package
"""
import sys


def get_font():
    """
    :return: (str) platform dependent unicode-font name
    """
    if sys.platform == 'win32':
        # Windows x32/x64
        fontname = 'Arial'
    elif sys.platform == 'linux2':
        # Linux (2.6 kernel):
        fontname = 'DejaVu Sans'
    elif sys.platform == 'darwin':
        # Mac OS X (10.4, 10.5, 10.7, 10.8):
        fontname = 'Arial '
    else:
        # Fallback - another platform
        fontname = 'Arial'
    return fontname
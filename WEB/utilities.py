"""
Useful utilities that don't have any other home
"""

from flask import current_app

def debug():
    """When called, presents an interactive session on the web page."""
    assert current_app.debug == False, "Don't panic! You're here by request of debug()"
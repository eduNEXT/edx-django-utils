"""
Exceptions thrown by Hooks.
"""


class HookException(Exception):
    """
    Base exception for hooks. It is re-raised by the Pipeline Runner if any of
    the actions/filters that is executing raises it.
    """

    def __init__(self, message="", redirect_to=None, status_code=None):
        super().__init__()
        self.message = message
        self.redirect_to = redirect_to
        self.status_code = status_code

    def __str__(self):
        return "HookException: {}".format(self.message)

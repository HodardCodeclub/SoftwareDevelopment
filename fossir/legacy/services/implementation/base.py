

from flask import g, session
from werkzeug.exceptions import Forbidden

from fossir.core.logger import sentry_set_tags
from fossir.legacy.common.security import Sanitization
from fossir.util.string import unicode_struct_to_utf8


class ServiceBase(object):
    """
    The ServiceBase class is the basic class for services.
    """

    UNICODE_PARAMS = False
    CHECK_HTML = True

    def __init__(self, params):
        if not self.UNICODE_PARAMS:
            params = unicode_struct_to_utf8(params)
        self._params = params

    def _process_args(self):
        pass

    def _check_access(self):
        pass

    def process(self):
        """
        Processes the request, analyzing the parameters, and feeding them to the
        _getAnswer() method (implemented by derived classes)
        """

        g.rh = self
        sentry_set_tags({'rh': self.__class__.__name__})

        self._process_args()
        self._check_access()

        if self.CHECK_HTML:
            Sanitization.sanitizationCheck(self._params)
        return self._getAnswer()

    def _getAnswer(self):
        """
        To be overloaded. It should contain the code that does the actual
        business logic and returns a result (python JSON-serializable object).
        If this method is not overloaded, an exception will occur.
        If you don't want to return an answer, you should still implement this method with 'pass'.
        """
        raise NotImplementedError


class LoggedOnlyService(ServiceBase):
    def _check_access(self):
        if session.user is None:
            raise Forbidden("You are currently not authenticated. Please log in again.")

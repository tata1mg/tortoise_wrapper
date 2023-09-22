from tortoise_wrapper.constants.http import HTTPStatusCodes


class BaseSanicException(Exception):
    def __init__(
        self,
        error,
        status_code=HTTPStatusCodes.BAD_REQUEST.value,
        meta=None,
        quiet=True,
        error_id=None,
        code=None,
    ):
        self._error = error
        self._status_code = status_code
        self._meta = meta
        self._quiet = quiet
        self._id = error_id
        self._code = code
        super().__init__()

    @property
    def error(self):
        return self._error

    @property
    def status_code(self):
        return self._status_code

    @property
    def meta(self):
        return self._meta

    @property
    def quiet(self):
        return self._quiet

    @property
    def error_id(self):
        return self._id

    @property
    def code(self):
        return self._code


class TaskExecutorException(BaseSanicException):
    def __init__(
        self,
        error,
        status_code=HTTPStatusCodes.BAD_REQUEST.value,
        meta=None,
        quiet=True,
    ):
        super().__init__(error, status_code, meta, quiet)


class HTTPInterServiceRequestException(BaseSanicException):
    def __init__(
        self,
        error,
        status_code=HTTPStatusCodes.BAD_REQUEST.value,
        meta=None,
        quiet=True,
        code=None,
        error_id=None,
    ):
        super().__init__(error, status_code, meta, quiet, error_id, code)


class HTTPRequestException(BaseSanicException):
    def __init__(
        self,
        error,
        status_code=HTTPStatusCodes.INTERNAL_SERVER_ERROR.value,
        meta=None,
        quiet=True,
    ):
        super().__init__(error, status_code, meta, quiet)


class HTTPRequestTimeoutException(BaseSanicException):
    def __init__(
        self,
        error,
        status_code=HTTPStatusCodes.REQUEST_TIMEOUT.value,
        meta=None,
        quiet=True,
    ):
        super().__init__(error, status_code, meta, quiet)


class BadRequestException(BaseSanicException):
    def __init__(
        self,
        error,
        status_code=HTTPStatusCodes.BAD_REQUEST.value,
        meta=None,
        quiet=True,
        error_id=None,
    ):
        super().__init__(error, status_code, meta, quiet, error_id)


class JsonDecodeException(BaseSanicException):
    def __init__(
        self,
        error,
        status_code=HTTPStatusCodes.INTERNAL_SERVER_ERROR.value,
        meta=None,
        quiet=True,
    ):
        super().__init__(error, status_code, meta, quiet)


class ForbiddenException(BaseSanicException):
    def __init__(self, error, status_code=403, meta=None, quiet=True):
        super().__init__(error, status_code, meta, quiet)

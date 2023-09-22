from enum import Enum

X_REQUEST_ID = "X-REQUEST-ID"
X_HEADERS = "X-HEADERS"
X_SHARED_CONTEXT = "X-SHARED-CONTEXT"


class HTTPStatusCodes(Enum):
    SUCCESS = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404
    FORBIDDEN = 403
    UNAUTHORIZED = 401
    MOVED_TEMPORARILY = 302
    INTERNAL_SERVER_ERROR = 500
    REQUEST_TIMEOUT = 408


class HTTPMethod(Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"


STATUS_CODE_MAPPING = {404: 400, 403: 401, 405: 400}

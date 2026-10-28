"""Supported HTTP Cats status codes and fallback descriptions"""

DESCRIPTIONS = {
    200: ("OK", "The request was successful."),
    201: ("Created", "The resource was successfully created."),
    301: ("Moved Permanently", "The resource has been permanently moved."),
    400: ("Bad Request", "The server could not process the request due to a client error."),
    401: ("Unauthorized", "Authentication is required to access this resource."),
    403: ("Forbidden", "The server refuses to fulfill the request."),
    404: ("Not Found", "The requested resource could not be found."),
    418: ("I'm a teapot", "The server refuses to brew coffee because it is a teapot."),
    429: ("Too Many Requests", "Too many requests were sent in a short period."),
    500: ("Internal Server Error", "The server encountered an unexpected condition."),
    502: ("Bad Gateway", "The server received an invalid response from an upstream server."),
    503: ("Service Unavailable", "The server is temporarily unavailable."),
    504: ("Gateway Timeout", "The server did not receive a timely response from an upstream server."),
    525: (
        "SSL Handshake Failed",
        "Cloudflare could not establish an SSL/TLS connection to the origin server. "
        "Possible causes include certificate, TLS configuration, or cipher issues.",
    ),
}

KNOWN_CODES = {
    100, 101, 102, 103,
    200, 201, 202, 203, 204, 205, 206, 207, 208, 214, 226,
    300, 301, 302, 303, 304, 305, 307, 308,
    400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410,
    411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421,
    422, 423, 424, 425, 426, 428, 429, 431, 444, 450, 451,
    495, 496, 497, 498, 499,
    500, 501, 502, 503, 504, 506, 507, 508, 509, 510, 511,
    521, 522, 523, 525, 530, 599,
}

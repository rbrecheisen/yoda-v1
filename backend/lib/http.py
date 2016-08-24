import base64

OK_200 = 200  # Request processed, entity returned
CREATED_201 = 201  # Request processed, entity created
ACCEPTED_202 = 202  # Request accepted for processing, not yet completed
NO_CONTENT_204 = 204  # Request processed but no content returned
BAD_REQUEST_400 = 400  # Client sent invalid request (e.g., missing params)
UNAUTHORIZED_401 = 401  # Not authenticated
FORBIDDEN_403 = 403  # Not authorized
NOT_FOUND_404 = 404  # Requested resource could not be found
METHOD_NOT_ALLOWED_405 = 405  # Request method not allowed for this resource
INTERNAL_SERVER_ERROR_500 = 500  # General error/exception server-side
NOT_IMPLEMENTED_501 = 501  # Server could not process request
BAD_GATEWAY_502 = 502  # Server is acting as gateway and received error from upstream
SERVICE_UNAVAILABLE_503 = 503  # Service temporarily unavailable

STRINGS = {
    200: 'OK_200 - Request processed, entity returned',
    201: 'CREATED_201 - Request processed, entity created',
    202: 'ACCEPTED_202 - Request accepted for processing, not yet completed',
    204: 'NO_CONTENT_204 - Request processed but no content returned',
    400: 'BAD_REQUEST_400 - Client sent invalid request, e.g., missing parameters',
    401: 'UNAUTHORIZED_401 - Client not authenticated or provided incorrect authentication details',
    403: 'FORBIDDEN_403 - Client is authenticated but not authorized to perform intended action',
    404: 'NOT_FOUND_404 - Requested resource not found on server',
    405: 'METHOD_NOT_ALLOWED_405 - Request method not allowed or available for this resource',
    500: 'INTERNAL_SERVER_ERROR_500 - General server-side error',
    501: 'NOT_IMPLEMENTED_501 - Server did not recognize HTTP method',
    502: 'BAD_GATEWAY_502 - Server is acting as a gateway and received error from upstream server',
    503: 'SERVICE_UNAVAILABLE_503 - Service temporarily unavailable',
}


# ----------------------------------------------------------------------------------------------------------------------
def code_to_str(code):
    return STRINGS[code]

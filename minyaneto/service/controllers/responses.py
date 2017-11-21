from flask import jsonify, make_response
import werkzeug


# success codes:
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_202_ACCEPTED = 202
HTTP_203_NON_AUTHORITATIVE_INFORMATION = 203
HTTP_204_NO_CONTENT = 204
HTTP_205_RESET_CONTENT = 205
HTTP_206_PARTIAL_CONTENT = 206

# client errors codes:
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZES = 401
HTTP_403_FORBIDDEN = 403
HTTP_404_PAGE_NOT_FOUND = 404
HTTP_405_METHOD_NOT_ALLOWED = 405
HTTP_410_GONE = 410

# server errors code:
HTTP_500_INTERNAL_SERVER_ERROR = 500


def _rest_response(code, obj=None):
    if not obj:
        obj = {}
    resp = jsonify(obj)
    resp.status_code = code
    return resp


# 200 + image:
def _image(image, content_type):
    response = make_response(image)
    response.headers['Content-Type'] = content_type
    return response

# 200 + jpeg image:
def jpeg(image):
    return _image(image, 'image/jpeg')

# 200 + png image:
def png(image):
    return _image(image, 'image/png')

# 200 + jpeg image:
def svg_xml(xml):
    return _image(xml, 'image/svg+xml')


# 200:
def ok(obj):
    return _rest_response(HTTP_200_OK, obj)


# 201:
def created(obj):
    return _rest_response(HTTP_201_CREATED, obj)


# 204:
def no_content():
    return _rest_response(HTTP_204_NO_CONTENT)


# 400:
def bad_request(error='Bad Request'):
    if isinstance(error, werkzeug.exceptions.BadRequest):
        error = error.description
    return _rest_response(HTTP_400_BAD_REQUEST,
                          {'status': HTTP_400_BAD_REQUEST, 'message': error})

# 401:
def unauthorized(error='Unauthorized'):
    if isinstance(error, werkzeug.exceptions.BadRequest):
        error = error.description
    return _rest_response(HTTP_401_UNAUTHORIZES,
                          {'status': HTTP_401_UNAUTHORIZES, 'message': error})

# 403:
def forbidden(error='Forbidden'):
    if isinstance(error, werkzeug.exceptions.Forbidden):
        error = error.description
    return _rest_response(HTTP_403_FORBIDDEN,
                          {'status': HTTP_403_FORBIDDEN, 'message': error})

# 404:
def not_found(error='Not Found'):
    if isinstance(error, werkzeug.exceptions.NotFound):
        error = error.description
    return _rest_response(HTTP_404_PAGE_NOT_FOUND,
                          {'status': HTTP_404_PAGE_NOT_FOUND, 'message': error})


# 405:
def method_not_allowed(error='Method Not Allowed'):
    if isinstance(error, werkzeug.exceptions.MethodNotAllowed):
        error = error.description
    return _rest_response(HTTP_405_METHOD_NOT_ALLOWED,
                          {'status': HTTP_405_METHOD_NOT_ALLOWED, 'message': error})


# 410:
def gone(error='The requested resource is no longer available at the server'):
    if isinstance(error, werkzeug.exceptions.Gone):
        error = error.description
    return _rest_response(HTTP_410_GONE, {'status': HTTP_410_GONE, 'message': error})


# 500:
def internal_server_error(error='Internal Server Error'):
    if isinstance(error, werkzeug.exceptions.InternalServerError):
        error = error.description
    return _rest_response(HTTP_500_INTERNAL_SERVER_ERROR,
                          {'status': HTTP_500_INTERNAL_SERVER_ERROR, 'message': error})

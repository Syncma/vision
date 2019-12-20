from bottle import request, response


def boilerplate_plugin(callback):
    def wrapper(*args, **kwargs):
        body = callback(*args, **kwargs)
        return {
            'code': response.status_code,
            'data': body,
        }

    return wrapper
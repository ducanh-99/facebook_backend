

def sucess():
    sucess = {
        "code": 1000,
        "message": "OK"
    }
    return sucess


def cannot_connect_db():
    res = {
        "code": 1001,
        "message": "Cannot connec to DB"
    }
    return res


def parameter_not_enough():
    res = {
        "code": 1002,
        "message": "Parameter is no enough"
    }
    return res


def parameter_type_invalid():
    res = {
        "code": 1003,
        "message": "Parameter type is invalid"
    }
    return res


def parameter_value_invalid():
    res = {
        "code": 1004,
        "message": "Parameter value is invalid"
    }
    return res


def unknow_error():
    res = {
        "code": 1005,
        "message": "Unknow Error"
    }
    return res


def file_size_too_big():
    res = {
        "code": 1006,
        "message": "File size is too big"
    }
    return res


def upload_file_failed():
    res = {
        "code": 1007,
        "message": "Upload file failde!"
    }
    return res


def maximum_number_of_images():
    res = {
        "code": 1008,
        "message": "Maximum number of images"
    }
    return res


def note_access():
    res = {
        "code": 1009,
        "message": "Not access"
    }
    return res


def action_done_previously():
    res = {
        "code": 1010,
        "message": "Action has been previously by this user"
    }
    return res


def post_is_not_exit():
    res = {
        "code": 9992,
        "message": "Post is not existed"
    }
    return res


def code_verify_is_incorret():
    res = {
        "code": 9993,
        "message": "Code verify is incorret"
    }
    return res


def no_or_end_data():
    res = {
        "code": 9994,
        "message": "No Data or end of list data"
    }
    return res


#
def user_is_not_validated():
    res = {
        "code": 9995,
        "message": "User is not validated"
    }
    return res


def user_existed():
    res = {
        "code": 9996,
        "message": "User existed"
    }
    return res


def method_is_invalid():
    res = {
        "code": 9997,
        "message": "Method is invalid"
    }
    return res


def token_is_invalid():
    res = {
        "code": 9998,
        "message": "Token is invalid"
    }
    return res


def exception_error():
    res = {
        "code": 9999,
        "message": "Exception error"
    }
    return res

def user_is_invalid():
    res = {
        "code": 10000,
        "message": "User is invalid"
    }
    return res

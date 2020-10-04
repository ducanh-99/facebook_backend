import json

def response_value (response, data):
    try:
        response["data"] = data
        return response
    except ValueError as e :
        raise print(e)

def remove_password_convert_dict(user):
    user = user.to_json()
    user = json.loads(user)
    del user["password"]
    return user

def format_response_post(response, data):
    try:
        data = json.loads(data)
        response["data"] = data
        response["data"]["is_block"] = False
        return response
    except ValueError as e:
        print(e)


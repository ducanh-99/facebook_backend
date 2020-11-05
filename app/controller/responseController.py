import json
import app.util.response as response
from bson import ObjectId


def response_value(response, data):
    try:
        response["data"] = data
        return response
    except ValueError as e:
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
        return response
    except ValueError as e:
        print(e)
def convert_object_to_dict(data):
    data = data.to_json()
    data = json.loads(data)
    return data


def convert_string_to_objectId(data):
    data = json.dumps(data)
    d = json.loads(data)
    print(d["owner"])
    d["owner"] = ObjectId(d["owner"])
    return json.dumps(d)


def update_post(post, body):
    body = json.dumps(body)
    body = json.loads(body)
    for i in body:
        if i == "owner":
            continue
        if i == "is_block":
            if body[i] != post.is_block:
                post.is_block = body[i]
            continue
        if i == "is_like":
            if body[i] != post.is_like:
                post.is_like = body[i]
            continue
        if body[i] != post[i]:
            post[i] = body[i]
    return post


def like_convert(post):
    res = {}
    res = response.sucess()
    res["like"] = post.like
    return res

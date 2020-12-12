from flask import Response, request, jsonify, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
import json

from app.model.user import User
from ..model.conversation import Conversation, Message
import app.controller.responseController as resCon
import app.util.response as response

from app.controller.validation import is_block


def get_list_embedded(current_user_id, user_id):
    current_user = User.objects().get(id=current_user_id)
    user = User.objects().get(id=user_id)
    current_user = current_user.get_user_embedded()
    user = user.get_user_embedded()
    list_user = [current_user, user]
    return list_user


def remove_user(conversation, user_id):
    received = {}
    for i in conversation["users"]:
        if str(i["user"]) != user_id:
            received = i
            del conversation["users"]
            conversation["received"] = received
    return conversation


class GetListConversationApi(Resource):

    @jwt_required
    def post(self):
        res = {}
        try:
            current_user_id = get_jwt_identity()
            conversations = Conversation.objects()
            data = []
            for conversation in conversations:
                if conversation.check_user(current_user_id):
                    conversation = json.loads(conversation.to_json())
                    conversation = remove_user(conversation, current_user_id)
                    conversation = self.get_last_message(conversation)
                    if conversation:
                        data.append(conversation)
            return jsonify(data)
        except Exception:
            raise Exception
            res = response.internal_server()
        return jsonify(res)

    def get_last_message(self, conversation):
        message = conversation["messages"]
        if len(message) == 0:
            return False
        last_message = message[-1]
        del conversation["messages"]
        conversation["last_messages"] = [last_message]
        return conversation


class GetConversationApi(Resource):

    @jwt_required
    def post(self, received_id):
        res = {}
        try:
            current_user_id = get_jwt_identity()
            users = get_list_embedded(current_user_id, received_id)
            conversation = Conversation.objects.get_users(
                users).first().to_json()
            conversation = json.loads(conversation)
            conversation = remove_user(conversation, current_user_id)
            conversation = json.dumps(conversation)
            return Response(conversation, mimetype="application/json")
        except Exception:
            res = response.internal_server()
        return jsonify(res)

    @jwt_required
    def delete(self, received_id):
        res = {}
        try:
            current_user_id = get_jwt_identity()
            users = get_list_embedded(current_user_id, received_id)
            conversation = Conversation.objects.get_users(
                users).first().delete()
            res = response.sucess()
            # return Response(conversation, mimetype="application/json")
        except Exception:
            res = response.internal_server()
        return jsonify(res)


class MessageApi(Resource):

    @jwt_required
    def post(self, received_id):
        res = {}
        try:
            from_user = get_jwt_identity()
            users = get_list_embedded(from_user, received_id)
            conversation = Conversation.objects.get_users(
                users).first()
            if conversation == None:
                conversation = self.create_conversation(from_user, received_id)
            to_user = received_id
            is_block(user_id=from_user, other_user_id=to_user)

            body = request.get_json()
            text = body["text"]
            index = conversation.get_index()

            message = self.create_message(from_user, to_user, text, index)
            conversation.update(push__messages=message)

            return Response(conversation.to_json(), mimetype="application/json")
        except response.NotAccess:
            res = response.not_access()
        except Exception:
            raise Exception
            res = response.internal_server()
        return jsonify(res)

    def create_message(self, from_user, to_user, text, index):
        message = Message()
        message.from_user = from_user
        message.to_user = to_user
        message.text = text
        message.index = index
        return message

    def create_conversation(self, user_id, received_id):
        users = get_list_embedded(user_id, received_id)
        conversation = Conversation(users=users).save()
        print(conversation)
        return conversation

    @jwt_required
    def delete(self, received_id):
        res = {}
        try:
            from_user = get_jwt_identity()
            users = get_list_embedded(from_user, received_id)
            conversation = Conversation.objects.get_users(
                users).first()
            if conversation == None:
                raise Exception
            body = request.get_json()
            index = body["index"]
            message = conversation.get_message_by_index(index)
            if message != None:
                conversation.update(pull__messages=message)
                res = response.sucess()
        except Exception:
            res = response.internal_server()
        return jsonify(res)


class GetMessageConversationApi(Resource):

    @ jwt_required
    def post(self, user_id):
        res = {}
        try:
            current_user_id = get_jwt_identity()
            list_user = get_list_embedded(current_user_id, user_id)
            conversations = Conversation.objects()
            for conversation in conversations:
                if conversation.check_list_user(list_user):
                    res = json.loads(conversation.to_json())
                    break
        except Exception:
            res = response.internal_server
        return jsonify(res)


class CreateAllConversation(Resource):
    def get(self):
        con = Conversation.objects().to_json()
        return Response(con, mimetype="application/json")

    def post(self):
        users = User.objects()
        print(users[0].get_user_embedded())
        for i in range(len(users)):
            current_user = users[i].get_user_embedded()
            for j in range(i, len(users)):
                user_2 = users[j].get_user_embedded()
                list_user = [current_user, user_2]
                conversation = Conversation.objects(users=list_user)
                conversation = json.loads(conversation.to_json())
                if not conversation:
                    Conversation(users=list_user).save()
        return "ok"


class ReadedConversationApi(Resource):
    pass


class ConversationApi(Resource):

    @ jwt_required
    def get(self, received_id):
        try:
            # user = resCon.get_user_name(json.loads(
            #     User.objects.get(id=received_id).to_json()))
            conversation = Conversation.objects.get(id=received_id)
            session["test"] = received_id
            res = []
            for i in session:
                res.append(i)
                print(i)
            res.append(session["test"])
            return res
        except Exception:
            pass

    @ jwt_required
    def post(self, received_id):
        res = {}
        try:
            send_id = get_jwt_identity()
            body = request.get_json()
            received = resCon.get_user_name(json.loads(
                User.objects.get(id=received_id).to_json()))
            sender = resCon.get_user_name(json.loads(
                User.objects.get(id=send_id).to_json()))

            users = [received, sender]

            message = Message()
            message.from_user = send_id
            message.to_user = received_id
            message.text = body["message"]

            messages = [message]

            Conversation.objects.get(users=users)
            res = response.user_existed()
        except DoesNotExist:
            conversation = Conversation(
                users=users, messages=messages).save()
            session["chat"] = str(conversation.id)
            res = response.sucess()
        except Exception:
            raise Exception
            res = response.internal_server()
        return jsonify(res)

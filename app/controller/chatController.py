from flask import Response, request, jsonify, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
import json

from app.model.user import User
from ..model.conversation import Conversation, Message
import app.controller.responseController as resCon
import app.util.response as response


def get_list_embedded(current_user_id, user_id):
    current_user = User.objects().get(id=current_user_id)
    user = User.objects().get(id=user_id)
    current_user = current_user.get_user_embedded()
    user = user.get_user_embedded()
    list_user = [current_user, user]
    return list_user


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


class GetMessageConversationApi(Resource):

    @jwt_required
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

    @jwt_required
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

    @jwt_required
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
            conversation = Conversation(users=users, messages=messages).save()
            session["chat"] = str(conversation.id)
            res = response.sucess()
        except Exception:
            raise Exception
            res = response.internal_server()
        return jsonify(res)

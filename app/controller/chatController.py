from flask import Response, request, jsonify, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
import json

from app.model.user import User
from ..model.conversation import Conversation, Message
import app.controller.responseController as resCon
import app.util.response as response


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
                    data.append(self.get_last_message(conversation))
                    print("dung vay ddmm")
            return jsonify(data)
        except Exception :
            raise Exception
            res = response.internal_server()
        return jsonify(res)

    def get_last_message(self, conversation):
        message = conversation["messages"]
        last_message = message[-1]
        conversation["messages"] = [last_message]
        return conversation




class GetMessageConversationApi(Resource):
    pass


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

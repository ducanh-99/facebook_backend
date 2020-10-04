from flask import Response, request, jsonify
from flask_restful import Resource
from mongoengine.errors import DoesNotExist

from app.model.user import User
from app.util.errors import InternalServerError
import app.util.response as response

CODE_VERIFY = 123456


class GetVerifyApi(Resource):
    res = {}

    def get(self):
        try:
            body = request.get_json()
            user = User.objects.get(phonenumber=body.get('phonenumber'))
            if user.verify:
                raise response.HaveDoneVerify
            self.res = response.sucess()
        except response.HaveDoneVerify:
            self.res = response.action_done_previously()
        except DoesNotExist:
            self.res = response.user_is_not_validated()
        except Exception:
            self.res = response.internal_server()
        return jsonify(self.res)

    def post(self):
        try:
            body = request.get_json()
            user = User.objects.get(phonenumber=body.get('phonenumber'))
            if user.verify:
                raise response.HaveDoneVerify
            if body.get('code_verify') != CODE_VERIFY:
                raise response.ParameterValueInvalid
            user.verify = True
            user.save()
            self.res = response.sucess()
        except response.HaveDoneVerify:
            self.res = response.user_existed()
        except response.ParameterValueInvalid:
            self.res = response.parameter_value_invalid()
        except DoesNotExist:
            self.res = response.user_is_not_validated()
        except Exception:
            self.res = response.internal_server()
        return jsonify(self.res)
        

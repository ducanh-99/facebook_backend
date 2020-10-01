from flask import Response, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
import datetime

from app.model.user import User
from app.util.errors import SchemaValidationError, NumberAlreadyExistsError, UnauthorizedError, \
    InternalServerError
from app.controller.responseController import response_value, remove_password_convert_dict
import app.util.response as response


class SignupApi(Resource):
    _res = {}

    def post(self):
        try:
            body = request.get_json()
            user = User(**body)
            user.hash_password()
            user.default()

            data = remove_password_convert_dict(user)
            self._res = response.sucess()
            self._res = response_value(self._res, data)
            user.save()
            return jsonify(self._res)
        except FieldDoesNotExist:
            raise SchemaValidationError
        except NotUniqueError:
            self._res = response.user_existed()
            return jsonify(self._res)
        except Exception as e:
            raise InternalServerError


class LoginApi(Resource):
    res = {}

    def post(self):
        try:
            body = request.get_json()
            user = User.objects.get(phonenumber=body.get('phonenumber'))
            authorized = user.check_password(body.get('password'))
            if not authorized:
                raise UnauthorizedError
            expires = datetime.timedelta(days=7)
            access_token = create_access_token(
                identity=str(user.id), expires_delta=expires)

            data = remove_password_convert_dict(user)
            self.res = response.sucess()
            self.res = response_value(self.res, data)
            self.res["data"]["token"] = access_token

            return jsonify(self.res)
        except (UnauthorizedError, DoesNotExist):
            self.res = response.user_is_not_validated()
            return jsonify(self.res)
        except Exception as e:
            raise InternalServerError


class LogoutApi(Resource):
    res = {}

    @jwt_required
    def post(self):
        try:
            user_id = get_jwt_identity()
            self.res = response.sucess()
            return jsonify(self.res)
        except Exception:
            raise InternalServerError



    

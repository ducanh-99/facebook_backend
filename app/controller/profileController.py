from flask import Response, request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
import werkzeug
import os
import uuid

from app.model.user import User
import app.util.response as response


UPLOAD_FOLDER = 'static/avt'
parser = reqparse.RequestParser()
parser.add_argument(
    'file', type=werkzeug.datastructures.FileStorage, location='files')


class AvtUploadApi(Resource):
    decorators = []
    res = {}

    @jwt_required
    def post(self):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            data = parser.parse_args()
            if data['file'] == "":
                return {
                    'data': '',
                    'message': 'No file found',
                    'status': 'error'
                }
            photo = data['file']

            if photo:
                filename = str(uuid.uuid4().hex) + '.png'
                user.avatar = UPLOAD_FOLDER + '/' + filename
                user.save()
                photo.save(os.path.join(UPLOAD_FOLDER, filename))
                self.res = response.sucess()
        except Exception:
            self.res = response.upload_file_failed()
        return jsonify(self.res)

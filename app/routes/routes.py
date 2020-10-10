from app.controller.test import TestApi
from app.controller.auth import SignupApi, LoginApi, LogoutApi
from app.controller.verifyController import GetVerifyApi
from app.controller.postController import PostApi, PostsApi
from app.controller.profileController import AvtUploadApi


def initialize_routes(api):
    api.add_resource(TestApi, '/api/test')
    # auth
    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')
    api.add_resource(LogoutApi, '/api/auth/logout')
    api.add_resource(GetVerifyApi, '/api/auth/verify')
    # post
    api.add_resource(PostsApi, '/api/post')
    api.add_resource(PostApi, '/api/post/<id>')
    # 
    api.add_resource(AvtUploadApi, '/api/upload_avt')

from app.controller.test import TestApi
from app.controller.auth import SignupApi, LoginApi, LogoutApi
from app.controller.verifyController import GetVerifyApi


def initialize_routes(api):
    api.add_resource(TestApi, '/api/test')

    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')
    api.add_resource(LogoutApi, '/api/auth/logout')
    api.add_resource(GetVerifyApi, '/api/auth/verify')

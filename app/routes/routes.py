from app.controller.test import TestApi
from app.controller.auth import SignupApi, LoginApi


def initialize_routes(api):
    api.add_resource(TestApi, '/api/test')

    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')

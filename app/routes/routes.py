from app.controller.test import TestApi

def initialize_routes(api):
    api.add_resource(TestApi, '/api/test')



from app.controller.test import TestApi
from app.controller.auth import SignupApi, LoginApi, LogoutApi
from app.controller.verifyController import GetVerifyApi
from app.controller.postController import PostApi, PostsApi
from app.controller.profileController import AvtUploadApi, AvatarApi
from app.controller.likeController import LikeApi, DislikeApi
from app.controller.commentController import PostCommentApi
from app.controller.friendController import ConfirmApi, RequestApi, ListRequestApi

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
    # avtar
    api.add_resource(AvtUploadApi, '/api/upload_avt')
    api.add_resource(AvatarApi, '/api/get_avt/<id>')
    # like
    api.add_resource(LikeApi, "/api/like/<id>")
    api.add_resource(DislikeApi, "/api/dislike/<id>")
    # comment
    api.add_resource(PostCommentApi, '/api/comment/<id>')
    # friends
    api.add_resource(ConfirmApi, "/api/friend/confirm/<id>")
    api.add_resource(RequestApi, "/api/friend/request/<id>")
    api.add_resource(ListRequestApi, "/api/friend/listrequest/<id>")

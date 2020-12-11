from app.controller.test import TestApi
from app.controller.auth import SignupApi, LoginApi, LogoutApi, ChangePasswordApi, Noti
from app.controller.verifyController import GetVerifyApi
from app.controller.postController import PostApi, PostsApi, UserPostsApi, VideoRetrievalApi, ImagesRetrievalApi, VideoListApi
from app.controller.profileController import AvtUploadApi, AvatarApi, ProfileApi, UpdateProfileApi
from app.controller.likeController import LikeApi, DislikeApi
from app.controller.commentController import PostCommentApi
from app.controller.friendController import ConfirmApi, RequestApi, ListRequestApi, BlockApi, ListFriendApi, ListBlockApi, ListSentRequestApi, RejectApi, RecommendFriendApi
from app.controller.searchController import SearchApi
from app.controller.chatController import ConversationApi, GetListConversationApi, CreateAllConversation, GetMessageConversationApi, GetConversationApi, MessageApi
from app.controller.notificationController import NotificationsApi, NotificationApi
from app.controller.InitController import Init


def initialize_routes(api):
    api.add_resource(TestApi, '/api/test')
    # auth
    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')

    api.add_resource(ChangePasswordApi, '/api/auth/changepassword')
    api.add_resource(LogoutApi, '/api/auth/logout')
    api.add_resource(GetVerifyApi, '/api/auth/verify')
    # post
    api.add_resource(PostsApi, '/api/post')
    api.add_resource(PostApi, '/api/post/<id>')
    api.add_resource(UserPostsApi, '/api/post/user/<user_id>')

    api.add_resource(VideoRetrievalApi, '/api/video/<post_id>')
    api.add_resource(ImagesRetrievalApi, '/api/post/<post_id>/<image_id>')

    # avatar
    api.add_resource(AvtUploadApi, '/api/upload_avt')
    api.add_resource(AvatarApi, '/api/get_avt/<id>')
    # like
    api.add_resource(LikeApi, "/api/like/<id>")
    api.add_resource(DislikeApi, "/api/dislike/<id>")
    # comment
    api.add_resource(PostCommentApi, '/api/comment/<post_id>')

    # friends
    api.add_resource(ConfirmApi, "/api/friend/confirm/<id>")
    api.add_resource(RejectApi, '/api/friend/reject/<sender_id>')
    api.add_resource(RequestApi, "/api/friend/request/<id>")
    api.add_resource(BlockApi, '/api/friend/block/<block_id>')

    api.add_resource(ListRequestApi, "/api/friend/listrequest")
    api.add_resource(ListFriendApi, '/api/friend/list_friend/<user_id>')
    api.add_resource(ListBlockApi, '/api/friend/list_block')
    api.add_resource(ListSentRequestApi, '/api/friend/list_sent_request')

    api.add_resource(RecommendFriendApi, '/api/friend/recommend')
    # Search
    api.add_resource(SearchApi, "/api/search")

    # profile
    api.add_resource(ProfileApi, '/api/profile/<user_id>')
    api.add_resource(UpdateProfileApi, '/api/update_profile')

    # chat
    api.add_resource(ConversationApi, '/api/chat/<received_id>')
    api.add_resource(GetListConversationApi, '/api/get_list_chat')
    api.add_resource(GetConversationApi, '/api/get_chat/<conversation_id>')
    api.add_resource(CreateAllConversation, "/api/create")
    api.add_resource(GetMessageConversationApi, "/api/<user_id>")

    api.add_resource(MessageApi, '/api/message/<conversation_id>')
    # video
    api.add_resource(VideoListApi, '/api/video')

    # init
    api.add_resource(Noti, "/test_noti")
    api.add_resource(Init, "/api/init")

    # noti
    api.add_resource(NotificationsApi, "/api/noti")
    api.add_resource(NotificationApi, "/api/noti/<noti_id>")

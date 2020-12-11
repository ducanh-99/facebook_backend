from app.model.user import User
from app.model.friends import Friend
import app.util.response as response


def is_block(user_id, other_user_id):
    friend_user = Friend.objects.get(owner=user_id)
    friend_other_user = Friend.objects.get(owner=other_user_id)

    if friend_other_user.is_blocked(user_id) or friend_user.is_blocked(other_user_id):
        print("test")
        raise response.NotAccess

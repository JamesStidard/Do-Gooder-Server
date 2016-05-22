

def detailed_user_view(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'email_confirmed': user.email_confirmed,
        'type': user.type,
    }


def user_view(user):
    return {
        'id': user.id,
        'username': user.username,
    }

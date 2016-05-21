

def detailed_user_view(user):
    return {
        'id': user.id,
        'email': user.email,
        'email_confirmed': user.email_confirmed,
    }


def user_view(user):
    return {
        'id': user.id,
        'email': user.email,
    }

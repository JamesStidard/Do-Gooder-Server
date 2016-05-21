

def sign_out(context: 'micro_context'):
    """
    Sign user out of auth and give client logout url for others.
    """
    context.set_current_user(None)

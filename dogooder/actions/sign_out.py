

def sign_out(context: 'micro_context') -> None:
    """
    Sign user out of auth and give client logout url for others.
    """
    context.current_user_id = None

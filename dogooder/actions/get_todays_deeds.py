from dogooder.model.deed import Deed
from dogooder.views.accomplishment import accomplishment_view


def get_todays_deeds(context: 'micro_context', timezone: str=None):
    with context.session as session:
        user  = context.current_user
        deeds = Deed.todays_accomplishments(session, timezone=timezone)
        return [accomplishment_view(deed, user=user) for deed in deeds]

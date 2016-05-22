from dogooder.model.deed import Deed
from dogooder.views.deed import deed_view


def get_deeds(context: 'micro_context') -> list:
    with context.session as session:
        deeds = session.query(Deed).all()
        return [deed_view(deed) for deed in deeds]

from dogooder.model.deed import Deed
from dogooder.model.accomplishment import Accomplishment
from dogooder.views.accomplishment import accomplishment_view


def insert_accomplishment(context: 'micro_context', deed_id: int, timezone: str=None):  # noqa
    with context.session as session:
        todays_deeds = Deed.todays_deeds(session, timezone=timezone)

        try:
            deed = [d for d in todays_deeds if d.id == deed_id][0]
        except IndexError:
            raise Exception('Deed not eligable for complition today.')
        else:
            user = context.current_user

            if user.id in [a.user_id for a in deed.todays_accomplishments]:
                raise Exception('Deed already accomplished today')

            accomplishment = Accomplishment(deed=deed, user=user)
            session.add(accomplishment)
            session.commit()

            result = [accomplishment_view(deed, user=user) for deed in todays_deeds]  # noqa
            context.broadcast('ACCOMPLISHMENT_INSERT', result)
            return result

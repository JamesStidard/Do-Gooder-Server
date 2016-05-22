from tornado.web import HTTPError

from dogooder.model.deed import Deed


def delete_deed(context: 'micro_context', id: int) -> bool:
    with context.session as session:
        count = session.query(Deed)\
                       .filter(Deed.id == id)\
                       .delete(synchronize_session=False)
        if count:
            context.broadcast('DEED_DELETE', id)
            return True
        else:
            raise HTTPError(404)

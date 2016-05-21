

def accomplishment_view(deed, *, user):
    accomplished = user in [a.user_id for a in deed.todays_accomplishments]

    return {
        'id': deed.id,
        'description': deed.description,
        'accomplished': accomplished,
        'accomplished_count': len(deed.todays_accomplishments),
    }

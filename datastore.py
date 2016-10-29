from pymongo import MongoClient
client = MongoClient('localhost:56327', connect=False)
db = client.bevager
rums = db.rums


def get_user():
    return rums.distinct('user')[0]


def persist_rum_for_user(rum, user):
    rum['user'] = user
    return rums.replace_one(
        {
            'user': rum['user'],
            'name': rum['name'],
            'country': rum['country'],
        },
        rum,
        upsert=True,
    )


def fetch_rum_for_user(rum, user):
    rum['user'] = user
    return rums.find_one({
        'user': rum['user'],
        'name': rum['name'],
        'country': rum['country'],
    })


def fetch_rums_for_user(user):
    return rums.find({'user': user})


def fetch_unrequested_by_all():
    users = rums.distinct('user')

    unrequested_lists = [
        rums.find({'signed': 'UNREQUESTED', 'user': user})
        for user in users
    ]

    unrequested_name_sets = [
        {rum['name'] for rum in unrequested_list}
        for unrequested_list in unrequested_lists
    ]

    unrequested_names = unrequested_name_sets[0].intersection(*unrequested_name_sets[1:])

    return rums.find({'user': users[0], 'name': {'$in': list(unrequested_names)}})

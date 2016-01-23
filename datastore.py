from pymongo import MongoClient
client = MongoClient()
db = client.bevager
rums = db.rums


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

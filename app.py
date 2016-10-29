import logging

from flask import Flask, jsonify, render_template

from datastore import (
    fetch_rums_for_user,
    fetch_unrequested_by_all,
    get_user,
)

logging_handler = logging.FileHandler('/var/log/bevager/bevager.log')
logging_handler.setLevel(logging.INFO)
logging_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))

app = Flask('bevager')
app.logger.addHandler(logging_handler)


@app.route('/health')
def health():
    return 'OK'


@app.route('/dashboard')
def dashboard():
    return render_template('index.html', username=get_user())


@app.route('/api/users/<user>')
def user(user):
    rums = [
        {
            key: rum[key]
            for key in rum.keys()
            if key != '_id'
        }
        for rum in fetch_rums_for_user(user)
    ]
    return jsonify({
        'rums': rums,
    })


@app.route('/api/global_unrequested')
def global_unrequested():
    rums = [
        {
            key: rum[key]
            for key in rum.keys()
            if key != '_id'
        }
        for rum in fetch_unrequested_by_all()
    ]
    return jsonify({
        'rums': rums,
    })


if __name__ == '__main__':
    app.run()

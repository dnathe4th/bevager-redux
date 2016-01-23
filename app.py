from flask import Flask, jsonify, render_template

from datastore import fetch_rums_for_user

app = Flask('bevager')


@app.route('/health')
def health():
    return 'OK'


@app.route('/dashboard')
def dashboard():
    return render_template('index.html')


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


if __name__ == '__main__':
    app.run()

import sqlite3
from datetime import date
import time

from flask import Flask, render_template, jsonify, request, g
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

DATABASE = 'db.sqlite'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def hello_world():
    return render_template('index.html')


# api -------------------------------------------------
@app.route('/api/houses')
def get_houses():
    cursor = get_db().cursor()

    house_data = []

    for row in cursor.execute('SELECT * FROM houses'):
        house_data.append({'id': row[0], 'name': row[1], 'house_url': row[2]})

    return jsonify(house_data)


@app.route('/api/prices')
def get_prices():
    cursor = get_db().cursor()

    price_data = []

    for row in cursor.execute('SELECT * FROM prices'):
        price_data.append(
            {'id': row[0], 'price': row[1], 'house_id': row[2], 'scraped_date': row[3]})

    return jsonify(price_data)


@app.route('/api/prices/<int:house_id>')
def get_prices_by_id(house_id):
    cursor = get_db().cursor()

    price_data = []

    for row in cursor.execute('SELECT * FROM prices WHERE house_id=' + str(house_id) + ' ORDER BY date(scraped_date) ASC'):
        price_data.append(
            {'id': row[0], 'price': row[1], 'house_id': row[2], 'scraped_date': row[3]})

    return jsonify(price_data)


@app.route('/api/dates')
def get_dates():
    cursor = get_db().cursor()

    date_data = []

    for row in cursor.execute('SELECT * FROM dates'):
        date_data.append(
            {'id': row[0], 'date': row[1]})

    return jsonify(date_data)
# (api) -------------------------------------------------

# post --------------------------------------------------
@app.route('/api/houses/add', methods=['GET', 'POST'])
def add_houses():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'GET':
        return "Hmm... I love it! (404 Not Found)", 404
    else:
        req_data = request.get_json()

        cursor.execute("INSERT INTO houses(name, url) VALUES('" + req_data['name'] + "', '" + req_data['url'] + "')")
        db.commit()
        cursor.execute('SELECT * FROM houses WHERE name=\'' + req_data['name'] + '\'')


        return jsonify({'added_name': cursor.fetchone()})

@app.route('/api/houses/delete', methods=['GET', 'POST'])
def delete_houses():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'GET':
        return "Hmm... I love it! (404 Not Found)", 404
    else:
        req_data = request.get_json()

        cursor.execute("SELECT id FROM houses WHERE name='" + req_data['name'] + "'")

        id_to_delete = cursor.fetchone()[0]

        cursor.execute("DELETE FROM houses WHERE name='" + req_data['name'] + "'")
        db.commit()

        cursor.execute("DELETE FROM prices WHERE house_id=" + str(id_to_delete))
        db.commit()


        return jsonify({'deleted_name': req_data['name']})
# (post) --------------------------------------------------




if __name__ == '__main__':
    app.run(debug=True)

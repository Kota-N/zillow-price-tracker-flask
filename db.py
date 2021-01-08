import sqlite3

# Database

conn = sqlite3.connect('/var/www/html/zillow_price_tracker/db.sqlite')
cursor = conn.cursor()

cursor.execute(
    '''
      CREATE TABLE houses(
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        url TEXT UNIQUE
      )
    ''')

cursor.execute(
    '''
      CREATE TABLE prices(
        id INTEGER PRIMARY KEY,
        price TEXT,
        house_id INTEGER,
        scraped_date DATE,
        FOREIGN KEY(house_id) REFERENCES houses(id),
        FOREIGN KEY(scraped_date) REFERENCES dates(date)
      )
    ''')

cursor.execute(
    '''
      CREATE TABLE dates(
        id INTEGER PRIMARY KEY,
        date DATE DEFAULT CURRENT_DATE UNIQUE
      )
    ''')

cursor.execute('INSERT OR IGNORE INTO houses(name, url) VALUES(\'house1\', \'https://www.zillow.com/homedetails/174-Motsinger-Rd-Winston-Salem-NC-27107/5704244_zpid/\')')
cursor.execute('INSERT OR IGNORE INTO houses(name, url) VALUES(\'house2\', \'https://www.zillow.com/homedetails/4342-Rex-Ct-Winston-Salem-NC-27107/89798164_zpid/\')')
cursor.execute('INSERT OR IGNORE INTO houses(name, url) VALUES(\'house3\', \'https://www.zillow.com/homedetails/2309-Pebble-Creek-Rd-Winston-Salem-NC-27107/5834581_zpid/\')')
cursor.execute('INSERT OR IGNORE INTO houses(name, url) VALUES(\'house4\', \'https://www.zillow.com/homedetails/4140-Langden-Dr-Winston-Salem-NC-27107/5776095_zpid/\')')

cursor.execute('INSERT OR IGNORE INTO dates(date) VALUES(\'2021-01-01\')')
cursor.execute('INSERT OR IGNORE INTO dates(date) VALUES(\'2021-01-02\')')

cursor.execute(
    'INSERT INTO prices(price, house_id, scraped_date) SELECT \'$1,000\' AS price, houses.id, dates.date FROM houses, dates WHERE houses.name=\'house1\' AND dates.date=\'2021-01-01\'')
cursor.execute(
    'INSERT INTO prices(price, house_id, scraped_date) SELECT \'$2,000\' AS price, houses.id, dates.date FROM houses, dates WHERE houses.name=\'house2\' AND dates.date=\'2021-01-01\'')
cursor.execute(
    'INSERT INTO prices(price, house_id, scraped_date) SELECT \'$3,000\' AS price, houses.id, dates.date FROM houses, dates WHERE houses.name=\'house3\' AND dates.date=\'2021-01-01\'')
cursor.execute(
    'INSERT INTO prices(price, house_id, scraped_date) SELECT \'$4,000\' AS price, houses.id, dates.date FROM houses, dates WHERE houses.name=\'house4\' AND dates.date=\'2021-01-01\'')

cursor.execute(
    'INSERT INTO prices(price, house_id, scraped_date) SELECT \'$1,000\' AS price, houses.id, dates.date FROM houses, dates WHERE houses.name=\'house1\' AND dates.date=\'2021-01-02\'')
cursor.execute(
    'INSERT INTO prices(price, house_id, scraped_date) SELECT \'$2,000\' AS price, houses.id, dates.date FROM houses, dates WHERE houses.name=\'house2\' AND dates.date=\'2021-01-02\'')
cursor.execute(
    'INSERT INTO prices(price, house_id, scraped_date) SELECT \'$3,000\' AS price, houses.id, dates.date FROM houses, dates WHERE houses.name=\'house3\' AND dates.date=\'2021-01-02\'')
cursor.execute(
    'INSERT INTO prices(price, house_id, scraped_date) SELECT \'$4,000\' AS price, houses.id, dates.date FROM houses, dates WHERE houses.name=\'house4\' AND dates.date=\'2021-01-02\'')


conn.commit()
conn.close()

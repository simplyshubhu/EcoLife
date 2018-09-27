from flask import Flask, render_template, request, session, g, redirect, url_for
from DBcm import UseDatabase, ConnectionError, CredentialError, SQLError
from os import urandom
from time import sleep
import conf
import json
from boltiot import Bolt, Sms
import datetime


app = Flask(__name__)

app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'badcode',
                          'password': '@SH1612NI*watcode98',
                          'database': 'Elife', }

app.secret_key = urandom(50)


# @app.before_request
# def before_request():
#     g.user = None
#     if 'user' in session:
#         g.user = session['user']


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get("username"):
        return render_template("Ecolife.html")
    else:
        return render_template('sign-in.html')


@app.route('/Ecolife', methods=['POST'])
def logged_in():
    res = ()
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _sql = '''select *
            from  user_info
            where user_name = %(uname)s and
            password = %(pass)s;'''
            cursor.execute(
                _sql,
                {'uname': request.form['username'],
                    'pass': request.form['password']})
            user = cursor.fetchall()
            if user:
                if user[0][2] == request.form['password']:
                    session['username'] = user[0][1]
                    return render_template('Ecolife.html')
            else:
                return render_template('sign-in.html', invalid=True)
    except ConnectionError as err:
        print('Is your Database switched on? Error: ', str(err))
    except CredentialError as err:
        print('User-id/Password issues. Error: ', err)
    except SQLError as err:
        print('Is your Query correct? Error: ', err)
    except Exception as err:
        print('Something went wrong: ', err)


@app.route('/timer')
def timer():
    timer_data = {}
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _sql = '''select counter,stat from timer'''
            cursor.execute(_sql)
            res = cursor.fetchall()
            status = res[-1][1]
            start_time = res[-1][0]
            start_time = (datetime.datetime.min + start_time).time()
            time = start_time.strftime('%X')
            timer_data = {'time': time, 'status': status}
            json.dumps(timer_data)
    except ConnectionError as err:
        print('Is your Database switched on? Error: ', str(err))
    except CredentialError as err:
        print('User-id/Password issues. Error: ', err)
    except SQLError as err:
        print('Is your Query correct? Error: ', err)
    except Exception as err:
        print('Something went wrong: ', err)
    return json.dumps(timer_data)


@app.route('/gettimer', methods=['POST'])
def get_timer():
    jsdata = request.get_json()
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _sql = '''update timer set counter= %s,
            stat= %s
            order by tid desc limit 1'''
            cursor.execute(_sql,
                           (jsdata['time'],
                            jsdata['status']))
            print('counter updated')
    except ConnectionError as err:
        print('Is your Database switched on? Error: ', str(err))
    except CredentialError as err:
        print('User-id/Password issues. Error: ', err)
    except SQLError as err:
        print('Is your Query correct? Error: ', err)
    except Exception as err:
        print('Something went wrong: ', err)
    return jsdata['time']


@app.route('/laser')
def security():
    def laser():
        api_key = "b42f36a3-9e5b-440c-8fa4-c57de4e5c4ca"
        device_id = "BOLT3732040"
        mybolt = Bolt(api_key, device_id)
        sms = Sms(conf.SSID, conf.AUTH_TOKEN, conf.TO_NUMBER, conf.FROM_NUMBER)

        print(json.loads(mybolt.isOnline())['value'])
        while True:
            response = mybolt.analogRead('A0')
            data = json.loads(response)
            print(data['value'])
            try:
                sensor_value = int(data['value'])
                print(sensor_value)
                if sensor_value < 1020:
                    response = sms.send_sms(" an unwanted access")
                    response = mybolt.digitalWrite('0', 'HIGH')
                    sleep(20000)

            except Exception as e:
                print("error", e)
                sleep(10000)
    laser()
    return render_template('entry.html')


if __name__ == '__main__':
    app.run(debug=True)

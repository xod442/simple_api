'''
 _______  ___   __   __  _______  ___      _______    _______  _______  ___
|       ||   | |  |_|  ||       ||   |    |       |  |   _   ||       ||   |
|  _____||   | |       ||    _  ||   |    |    ___|  |  |_|  ||    _  ||   |
| |_____ |   | |       ||   |_| ||   |    |   |___   |       ||   |_| ||   |
|_____  ||   | |       ||    ___||   |___ |    ___|  |       ||    ___||   |
 _____| ||   | | ||_|| ||   |    |       ||   |___   |   _   ||   |    |   |
|_______||___| |_|   |_||___|    |_______||_______|  |__| |__||___|    |___|

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0.

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


__author__ = "@netwookie"
__credits__ = ["Rick Kauffman"]
__license__ = "Apache2"
__version__ = "0.1.1"
__maintainer__ = "Rick Kauffman"
__status__ = "Alpha"

'''
from flask import Flask, request, render_template, abort, redirect, url_for
import pymongo
import os
from jinja2 import Environment, FileSystemLoader
from bson.json_util import dumps
from bson.json_util import loads
#
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')
APP_TEMPLATE = os.path.join(APP_ROOT, 'templates')

config = {
    "username": "admin",
    "password": "siesta3",
    "server": "mongo",
}
# mongodump --uri="mongodb://{}:{}@{}".format(config["username"], config["password"], config["server"])
connector = "mongodb://{}:{}@{}".format(config["username"], config["password"], config["server"])
client = pymongo.MongoClient(connector)
db = client["demo2"]



'''
#-------------------------------------------------------------------------------
Login Section
#-------------------------------------------------------------------------------
'''

@app.route("/", methods=('GET', 'POST'))
def login():


        message = "Welcome to this simple API"
        return render_template('home.html', message=message)


'''
#-------------------------------------------------------------------------------
Home
#-------------------------------------------------------------------------------
'''

@app.route("/home", methods=('GET', 'POST'))
def home():

    my_customers = []
    cust = db.customer.find({})
    customer = loads(dumps(cust))
    for c in customer:
        number = c['number']
        name = c['name']
        phone = c['phone']
        email = c['email']

        info = [number, name, phone, email]
        my_customers.append(info)
    message = "Operation completed successfully"
    return render_template('home1.html', message=message, my_customers=my_customers)



'''
#-------------------------------------------------------------------------------
Contact Section
#-------------------------------------------------------------------------------
'''

@app.route("/add_customer", methods=('GET', 'POST'))
def add_customer():
    if request.method == 'POST':
        highest_record = db.customer.find({}).sort("number", pymongo.DESCENDING).limit(1)
        customer = loads(dumps(highest_record))
        if customer == []:
            number = 1
        else:
            number = customer[0]["number"] + 1

        entry = {
            "name": request.form['name'].replace('"', ""),
            "phone": request.form['phone'].replace('"', ""),
            "email": request.form['email'].replace('"', ""),
            "number": number,
        }
        # TODO: check to see if record exists
        response = db.customer.insert_one(entry)
        # TODO check to see record was written to database)
        message = 'Customer information written to database'
        return redirect(url_for('home', message=message))

    return render_template('add_customer.html')

@app.route("/list_customer", methods=('GET', 'POST'))
def list_customer():
    my_customers = []
    cust = db.customer.find({})
    customer = loads(dumps(cust))
    for c in customer:
        number = c['number']
        name = c['name']
        phone = c['phone']
        email = c['email']

        info = [number, name, phone, email]
        my_customers.append(info)
    # Check user credentials
    return render_template('list_customer.html', my_customers=my_customers)

@app.route("/edit_customer", methods=('GET', 'POST'))
def edit_customer():
    if request.method == 'POST':
        log_info = request.form['customer']
        if log_info == "unselected":
            message = "please select a valid customer"
            # Get a list of customers
            my_customers = []
            customer = db.customer.find({})
            cust = loads(dumps(customer))
            for item in cust:
                number = item['number']
                number = str(number)
                name = item['name']
                dash = '-'
                cust = number+dash+name
                my_customers.append(cust)
            return render_template('edit_customer.html', my_customers=my_customers, message=message)

        temp = log_info.split('-')
        number = temp[0]
        number = int(number)
        customer = db.customer.find({"number":number})
        cust = loads(dumps(customer))
        name = cust[0]['name']
        phone = cust[0]['phone']
        email = cust[0]['email']
        return render_template('edit_customer_complete.html', name=name, phone=phone, email=email, number=number)

    # Get a list of customers
    my_customers = []
    customer = db.customer.find({})
    cust = loads(dumps(customer))
    for item in cust:
        number = item['number']
        number = str(number)
        name = item['name']
        dash = '-'
        cust = number+dash+name
        my_customers.append(cust)
    return render_template('edit_customer.html', my_customers=my_customers)

@app.route("/edit_customer_complete", methods=('GET', 'POST'))
def edit_customer_complete():
    name = request.form['name'].replace('"', "")
    number = request.form['number'].replace('"', "")
    phone = request.form['phone'].replace('"', "")
    email = request.form['email'].replace('"', "")
    number = int(number)
    myquery = { "number": number }
    newvalues = { "$set": { "name": name, "phone": phone, "email": email }}
    db.customer.update_one(myquery, newvalues)
    message = 'Customer information been updated in the database'
    return redirect(url_for('home', message=message))

@app.route("/delete_customer", methods=('GET', 'POST'))
def delete_customer():
    if request.method == 'POST':
        cust = request.form['customer']
        if cust == "unselected":
            message = "please select a valid customer"
            return render_template('delete_customer.html', message=message)

        temp = cust.split('-')
        number = temp[0]
        number = int(number)
        meet = db.customer.delete_one({"number":number})
        message = "Customer entry has been deleted"
        return redirect(url_for('home', message=message))
    # Get a list of logs
    my_customer = []
    cust = db.customer.find({})
    cust = loads(dumps(cust))
    for item in cust:
        number = item['number']
        number = str(number)
        name = item['name']
        dash = '-'
        customer = number+dash+name
        my_customer.append(customer)
    return render_template('delete_customer.html', my_customer=my_customer)
'''
#-------------------------------------------------------------------------------
Magic 8 Ball
#-------------------------------------------------------------------------------
'''


@app.route("/magic", methods=('GET', 'POST'))
def magic():
    # Check user credentials
    return render_template('magic.html')

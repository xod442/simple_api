'''

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
from utility.client import get_client
#
app = Flask(__name__)

# A dictionary of the mongo database credentials
config = {
    "username": "admin",
    "password": "siesta3",
    "server": "mongo",
}

# Setup database connetor
connector = "mongodb://{}:{}@{}".format(config["username"], config["password"], config["server"])
client = pymongo.MongoClient(connector)

#set mongo database
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

    my_central = []
    info = db.central.find({})
    docs = loads(dumps(info))
    for d in docs:
        group_name = d['group_name']
        description = d['description']

        info2 = [number, group_name, description]
        my_central.append(info2)
    message = "Operation completed successfully"
    return render_template('home1.html', message=message, my_central=my_central)



'''
#-------------------------------------------------------------------------------
Contact Section
#-------------------------------------------------------------------------------
'''

@app.route("/add_group", methods=('GET', 'POST'))
def add_group():
    if request.method == 'POST':
        highest_record = db.central.find({}).sort("number", pymongo.DESCENDING).limit(1)
        highest = loads(dumps(highest_record))
        if high == []:
            number = 1
        else:
            number = customer[0]["number"] + 1

        entry = {
            "group_name": request.form['group_name'],
            "description": request.form['description'],
            "number": number,
        }
        # TODO: check to see if record exists
        response = db.central.insert_one(entry)
        # TODO check to see record was written to database)
        message = 'Group information written to database'
        return redirect(url_for('home', message=message))

    return render_template('add_group.html')

@app.route("/get_groups", methods=('GET', 'POST'))
def get_groups():
    
    central = get_client()

    my_central = []

    all_groups = Groups()

    response = all_groups.get_groups(conn=central)

    groups = (response['msg']['data'])


    # Check user credentials
    return render_template('get_groups.html', groups=groups)

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

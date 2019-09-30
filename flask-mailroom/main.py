import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations', methods=['POST', 'GET'])
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/create', methods=['GET', 'POST'])
def create():
    # get requests land us at /create
    if request.method == 'GET':
        return render_template('create.jinja2')

    # post request should query db for the donor, add donation, redir to /all
    if request.method == 'POST':
        donor = Donor(name=request.form['name'])
        print(donor)
        value = Donation(value=request.form['amount'])
        print(value)

        Donation(donor=donor, value=value).save()
        # saved_donation = Donation(
        #     donor=request.form['name'], value=request.form['amount'])
        #saved_donation.save()

        return redirect(url_for('all'))

    return render_template('create.jinja2', create=create)

    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port, debug=True)


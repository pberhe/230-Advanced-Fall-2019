import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import SavedTotal

app = Flask(__name__)
# app.secret_key = b'IT9_\x92\x06\xbdN\x03\xb8[\xf0\xe2\xab\xbf\x9fk0a\x1dS\xd0\x85\x85'
app.secret_key = os.environ.get('SECRET_KEY').encode()

@app.route('/add', methods=['GET', 'POST'])
def add():
    # session['total']
    if 'total' not in session:
        session['total'] = 0

    if request.method == 'POST':
        number = int(request.form['number'])
        session['total'] += number    

    return render_template('add.jinja2', session=session)

@app.route('/save', methods=['POST'])
def save():
    total = session.get('total', 0)
    code = base64.b32encode(os.urandom(8)).decode().strip('=')
    
    saved_total = SavedTotal(value=total, code=code)
    saved_total.save()

    return render_template('save.jinja2', code=code)

@app.route('/retrieve')
def retrieve():
    code = request.args.get('code', None)
    # If user is visiting the page (did not submit yet)
        # Then just render reterieve.jinja2 templste
    # But if they did submit:
        # Attempt retrieve saved total based on code
        # Then Save the total from that SavedTotal session
        # Then Redirect the user back to the 'add' page

    if code is None:
        return render_template('retrieve.jinja2')
    else:
        try: 
            saved_total = SavedTotal.get(SavedTotal.code == code)
        except SavedTotal.DoesNotExist: 
            return render_template('retreive.jinja2', error="Code not found.")
        session['total'] = saved_total.value

        return redirect(url_for('add'))
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

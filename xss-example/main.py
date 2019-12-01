import os
import base64
import random

from flask import Flask, request, session
from model import Message

app = Flask(__name__)

app.secret_key = '2cf74d0b395d4eb3bcf229fac11c46f8'


@app.route('/', methods=['GET', 'POST'])
def home():
    if 'csrf_token' not in session:
        session['csrf_token'] = str(random.randint(10000000, 99999999))

    if request.method == 'POST':
        m = Message(content=request.form['content'])
        m.save()

    body = """
<html>
<body>
<h1>Class Message Board</h1>
<h2>Contribute to the Knowledge of Others</h2>
<form method="POST">
    <textarea name="content"></textarea>
    <input type="submit" value="Submit">
    <input type="hidden" name="csrf_token" value="{}">
</form>
<h2>Wisdom From Your Fellow Classmates</h2>
"""

    for m in Message.select():
        body += """
<div class="message">
{}
</div>
""".format(session['csrf_token'], m.content.replace('<', '&lt;').replace('>', '&gt;'))

    return body


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

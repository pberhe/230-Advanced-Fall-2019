#!/usr/bin/env python

import datetime
import os
from flask import Flask

app = Flask(__name__)


@app.route('/')
def epoch_time():
    return str(datetime.datetime.now().timestamp())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6378))
    app.run(host="0.0.0.0", port=port, debug=True)
from SampleApp import app
from flask import render_template

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/otherpage')
def otherpage():
    return render_template('otherpage.html')
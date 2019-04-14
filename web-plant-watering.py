#!/usr/bin/env python2
from flask import Flask, render_template, redirect, url_for
import datetime
#import psutil
import SoilMoistureRead
import os

app = Flask(__name__)

def template(title="Plant Watering Control Panel", text=""):
    now = datetime.datetime.today()
    time = now.strftime("%A, %d. %B %Y %I:%M%p")
    template_date = {
        'title' : title,
        'time' : time,
        'text' : text
        }
    return template_date


@app.route("/")
def hello():
    template_data = template()
    return render_template('main.html', **template_data)


@app.route("/last_watered")
def check_last_watered():
    template_data = template(text=SoilMoistureRead.get_last_watered())
    return render_template('main.html', **template_data)


@app.route("/moisture")
def check_moisture():
    template_data = template(text="Current moisture is %d%%." % SoilMoistureRead.get_percent_wet())
    return render_template('main.html', **template_data)


@app.route("/water")
def water():
    template_data = template(text=SoilMoistureRead.main())
    return render_template('main.html', **template_data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

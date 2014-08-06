#
# Copyright 2014 ABC Startsiden
#
# Author: Morten Bekkelund <morten.bekkelund@startsiden.no>
#
#

import re
import urllib
import urllib2
import simplejson as json
from flask import Flask, render_template, request
from config import *

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def home():
    minions = salt_api("runner","manage.status")
    return render_template('home.html', minions=minions)

@app.route('/version')
def version():
    minions = salt_api("local","pkg.version",target="*",arg="salt-minion")
    return render_template('version.html', minions=minions)

@app.route('/grains')
def grains():
    minions = salt_api("local","grains.items",target="*")
    return render_template('grains.html', minions=minions)

@app.route('/pillars')
def pillars():
    minions = salt_api("local","pillar.raw",target="*")
    return render_template('pillars.html', minions=minions)

@app.route('/disk_percent')
def disk_percent():
    minions = salt_api("local","disk.percent",target="*")
    return render_template('disk_percent.html', minions=minions)

@app.route('/loadavg')
def loadavg():
    minions = salt_api("local","status.loadavg",target="*")
    return render_template('loadavg.html', minions=minions)

@app.route('/pkgsearch', methods=['GET', 'POST'])
def pkgsearch():
    arg = ""
    if request.method == "POST":
        arg = request.form['pkg']
    elif  request.method == "GET":
        arg = request.args.get('pkg')
    print request.args.get('pkg')
    minions = salt_api("local","pkg.version",target="*",arg=arg)
    return render_template('pkgsearch.html', minions=minions, pkg=arg)

@app.route('/full')
def full():
    minion = request.args.get('minion')
    salt_version = salt_api("local","pkg.version",target=minion,arg="salt-minion")
    grains = salt_api("local","grains.items",target=minion)
    pillars = salt_api("local", "pillar.raw",target=minion)
    return render_template('full.html', minion=minion, salt_version=salt_version, grains=grains, pillars=pillars)


def salt_api(client,function,**kwargs):
    """ call salt-api...
        "client" must be either "runner" or "local" 
        "target" is the salt-minion, for instance "*" (all) or "my-minion-name"
        "function" is the salt-python-function, for instance test.ping or pkg.version
        "arg" is the functions argument, for instance packagename (as in: pkg.version salt-minion)
    """
    arg = None
    target = None
    for k, v in kwargs.iteritems():
        if k == "arg":
            arg = v
        elif k == "target":
            target = v
        
    #url = "https://salt.startsiden.no:8000/run"
    url = app.config['SALT_API_URL']

    values = dict()
    values["client"] = client
    values["fun"] = function
    if target: values["tgt"] = target
    if arg: values["arg"] = arg
    values["username"] = app.config['SALT_USER']
    values["password"] = app.config['SALT_PASSWORD']
    values["eauth"] = "pam"

    data = urllib.urlencode(values)
    req  = urllib2.Request(url,data)
    res  = urllib2.urlopen(req)
    page = res.read()
    minions = json.loads(page)

    return minions['return'][0]


if __name__ == '__main__':
  app.run(debug=True,host='0.0.0.0')

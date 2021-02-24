from flask import render_template
from flask_login import login_required, current_user
from . import main
import os

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/setting', methods=['POST', 'GET'])
@login_required
def setting():
    return render_template('setting.html', current_user=current_user)

@main.route('/documentation')
def documentation():
    return 'yes'

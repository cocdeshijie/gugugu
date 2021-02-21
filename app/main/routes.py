from flask import request, render_template, jsonify
from flask_login import login_required, current_user
from . import main
import os
import secrets

APP_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../files/')

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/setting', methods=['POST', 'GET'])
@login_required
def setting():
    print(current_user.get_role())
    return render_template('setting.html')

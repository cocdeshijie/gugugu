from flask import render_template
from flask_login import login_required, current_user
from . import main
from.forms import DeleteGroupForm
from ..models import Group, User

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/setting', methods=['POST', 'GET'])
@login_required
def setting():
    return render_template('/setting/setting.html', current_user=current_user)

@main.route('/manage_group', methods=['POST', 'GET'])
@login_required
def manage_group():
    form = DeleteGroupForm()
    groups = Group.query.all()
    if form.validate_on_submit():
        print(form.group_id.data)
    return render_template('/setting/manage_group.html', current_user=current_user, groups=groups, form=form)

@main.route('/manage_group_user', methods=['POST', 'GET'])
@login_required
def manage_group_user():
    return render_template('/setting/manage_group_user.html', current_user=current_user)

@main.route('/manage_all_user', methods=['POST', 'GET'])
@login_required
def manage_all_user():
    return render_template('/setting/manage_all_user.html', current_user=current_user)

@main.route('/documentation')
def documentation():
    return 'yes'

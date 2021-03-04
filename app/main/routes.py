from flask import render_template, flash, redirect, url_for, Markup
from flask_login import login_required, current_user
from . import main
from.forms import DeleteGroupForm, CreateGroupForm
from ..models import Group, User
from .. import db

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
    delete_group_form = DeleteGroupForm()
    create_group_form = CreateGroupForm()
    groups = Group.query.all()
    if delete_group_form.validate_on_submit():
        group = Group.query.get(delete_group_form.group_id.data)
        flash([group.name + ' deleted.', 'Deleted'], 'secondary')
        for user in group.users:
            db.session.delete(user)
        db.session.delete(group)
        db.session.commit()
        return redirect(url_for('main.manage_group'))
    if create_group_form.validate_on_submit():
        new_group = Group(name=create_group_form.name.data, space_limits=create_group_form.space_limit.data)
        db.session.add(new_group)
        db.session.commit()
        flash([new_group.name + ' created.', 'Success'], 'success')
        return redirect(url_for('main.manage_group'))
    return render_template('/setting/manage_group.html',
                           current_user=current_user,
                           groups=groups,
                           delete_group_form=delete_group_form,
                           create_group_form=create_group_form)

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

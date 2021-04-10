from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from . import main
from.forms import DeleteGroupForm, CreateGroupForm, UserAccountForm, ManageGroupForm
from ..models import Group, User
from .. import db


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = UserAccountForm()
    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        if form.username.data and form.username.data != user.username:
            form.check_username()
            user.username = form.username.data
        if form.email.data and form.email.data != user.email:
            user.email = form.email.data
        if form.new_password.data:
            if not user.verify_password(form.old_password.data):
                flash(['Wrong password.', 'Error'], 'danger')
                return render_template('/setting/account.html',
                                       current_user=current_user,
                                       form=form)
            user.password = form.new_password.data
        db.session.commit()
        flash(['Saved.', 'Success'], 'success')
        return render_template('/setting/account.html',
                               current_user=current_user,
                               form=form)
    return render_template('/setting/account.html',
                           current_user=current_user,
                           form=form)


@main.route('/site_setting', methods=['POST', 'GET'])
@login_required
def site_setting():
    if not current_user.group.admin:
        flash(['You don\'t have access to this page.', 'Error'], 'danger')
        return redirect(url_for('main.index'))
    return render_template('/setting/site_setting.html')


@main.route('/manage_group', methods=['POST', 'GET'])
@login_required
def manage_group():
    if not current_user.group.admin:
        flash(['You don\'t have access to this page.', 'Error'], 'danger')
        return redirect(url_for('main.index'))
    delete_group_form = DeleteGroupForm()
    create_group_form = CreateGroupForm()
    manage_group_form = ManageGroupForm()
    groups = Group.query.all()
    if manage_group_form.submit.data and manage_group_form.validate_on_submit():
        group = Group.query.get(manage_group_form.group_id.data)
        group.name = manage_group_form.name.data
        group.space_limits = manage_group_form.space_limit.data
        group.extension_setting = manage_group_form.extension_setting.data
        group.extensions_input = manage_group_form.extensions.data
        db.session.commit()
        flash(['Saved.', 'Success'], 'success')
        return redirect(url_for('main.manage_group'))
    if create_group_form.create.data and create_group_form.validate_on_submit():
        new_group = Group(name=create_group_form.name.data,
                          space_limits=create_group_form.space_limit.data)
        db.session.add(new_group)
        db.session.commit()
        flash([new_group.name + ' created.', 'Success'], 'success')
        return redirect(url_for('main.manage_group'))
    if delete_group_form.group_id.data and delete_group_form.validate_on_submit():
        if len(groups) == 2:
            flash(['At least one group is needed.', 'Error'], 'danger')
            return redirect(url_for('main.manage_group'))
        group = Group.query.get(delete_group_form.group_id.data)
        flash([group.name + ' deleted.', 'Deleted'], 'secondary')
        for user in group.users:
            db.session.delete(user)
        db.session.delete(group)
        db.session.commit()
        return redirect(url_for('main.manage_group'))
    return render_template('/setting/manage_group.html',
                           current_user=current_user,
                           groups=groups,
                           delete_group_form=delete_group_form,
                           create_group_form=create_group_form,
                           manage_group_form=manage_group_form)


@main.route('/manage_user', methods=['POST', 'GET'])
@login_required
def manage_user():
    if not current_user.group.admin:
        flash(['You don\'t have access to this page.', 'Error'], 'danger')
        return redirect(url_for('main.index'))
    return render_template('/setting/manage_user.html',
                           current_user=current_user)


@main.route('/documentation')
def documentation():
    return 'yes'
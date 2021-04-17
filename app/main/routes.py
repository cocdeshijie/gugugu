from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from . import main
from.forms import DeleteGroupForm, CreateGroupForm, UserAccountForm, ManageGroupForm, ManageSiteForm, DeleteUserForm
from ..models import Group, User, SiteSetting
from .. import db
import json


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
                return redirect(url_for('main.account'))
            user.password = form.new_password.data
        db.session.commit()
        flash(['Saved.', 'Success'], 'success')
        return redirect(url_for('main.account'))
    return render_template('/setting/account.html',
                           current_user=current_user,
                           form=form)


@main.route('/site_setting', methods=['POST', 'GET'])
@login_required
def site_setting():
    site_setting = SiteSetting.query.get(1)
    form = ManageSiteForm()
    form.default_group.choices = [(group.id, group.name) for group in Group.query.all() if group.id != 1]
    form.default_group.default = site_setting.default_group_id
    form.process()
    if not current_user.group.admin:
        flash(['You don\'t have access to this page.', 'Error'], 'danger')
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        site_setting.title = form.site_title.raw_data[0]
        site_setting.site_description = form.site_description.raw_data[0]
        site_setting.guest_upload = False if not form.guest_upload.raw_data else True
        site_setting.api = False if not form.api.raw_data else True
        site_setting.default_group_id = int(form.default_group.raw_data[0])
        site_setting.default_file_location = 'local'
        db.session.commit()
        flash(['Saved.', 'Success'], 'success')
        return redirect(url_for('main.site_setting'))
    return render_template('/setting/site.html',
                           site_setting=site_setting,
                           form=form)


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
        group = Group.query.get(int(manage_group_form.group_id.data))
        group.name = manage_group_form.name.data
        group.space_limits = int(manage_group_form.space_limit.data)
        group.extension_setting = manage_group_form.extension_setting.data
        group.extensions_input = manage_group_form.extensions.data
        db.session.commit()
        flash(['Saved.', 'Success'], 'success')
        return redirect(url_for('main.manage_group'))
    if create_group_form.create.data and create_group_form.validate_on_submit():
        if Group.query.filter_by(name=create_group_form.name.data).first() is not None:
            flash(['Group {} exists.'.format(create_group_form.name.data), 'Error'], 'danger')
            return redirect(url_for('main.manage_group'))
        new_group = Group(name=create_group_form.name.data,
                          space_limits=create_group_form.space_limit.data)
        db.session.add(new_group)
        db.session.commit()
        flash(['Group {} created.'.format(new_group.name), 'Success'], 'success')
        return redirect(url_for('main.manage_group'))
    if delete_group_form.group_id.data and delete_group_form.validate_on_submit():
        if len(groups) == 2:
            flash(['At least one group is needed.', 'Error'], 'danger')
            return redirect(url_for('main.manage_group'))
        if int(delete_group_form.group_id.data) == json.loads(open('./app/files/config.json', 'r').read())['default_group_id']:
            flash(['Default group can not be deleted.', 'Error'], 'danger')
            return redirect(url_for('main.manage_group'))
        group = Group.query.get(delete_group_form.group_id.data)
        flash([group.name + ' deleted.', 'Deleted'], 'success')
        for user in group.users:
            db.session.delete(user)
        db.session.delete(group)
        db.session.commit()
        return redirect(url_for('main.manage_group'))
    return render_template('/setting/groups.html',
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
    users = User.query.all()
    delete_user_form = DeleteUserForm()
    if delete_user_form.user_id.data and delete_user_form.validate_on_submit():
        user = User.query.get(delete_user_form.user_id.data)
        flash(['User {} deleted'.format(user.username), 'Deleted'], 'success')
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('main.manage_user'))
    return render_template('/setting/users.html',
                           users=users,
                           delete_user_form=delete_user_form)


@main.route('/documentation')
def documentation():
    return 'yes'
from flask import abort, render_template, request

from sopy import db
from sopy.admin import bp
from sopy.admin.forms import EditUserGroupsForm
from sopy.ext.views import template, redirect_for
from sopy.auth.models import User, Group
from sopy.auth.login import has_group, current_user, login_required


@bp.before_request
@login_required
def authorize():
    """ Check that the user has privileges to access this page. """
    if not current_user.has_group('approved'):
        abort(403)  # page forbidden


@bp.route('/groups')
@template('admin/view_all_groups.html')
def view_all_groups():
    """ returns all distinct groups in the database, adds links to the page
    note: the links are not very pretty. """
    groups = Group.query.distinct()
    return {'groups': groups}


@bp.route('/groups/<group_name>', methods=['GET', 'POST'])
@template('/admin/view_group.html')
def view_group(group_name):
    """ Find all groups, and the users which belong to them. """
    selected_group = User.query.filter(User._groups.any(Group.name == group_name)).all()
    form = EditUserGroupsForm()
    if form.validate_on_submit():
        user = User.query.get(form.user_id.data)
        group = Group.query.filter_by(name=group_name).one()
        user._groups.add(group)
        db.session.commit()
        return redirect_for('admin.view_group', group_name=group_name)
    return {'group': group_name, 'group_users': selected_group, 'form': form}


@bp.route('/groups/<group_name>/remove/<int:user_id>')
def remove_user_from_group(group_name, user_id):
    """ remove a specified user from a group """
    user = User.query.get_or_404(user_id)
    group = Group.query.filter_by(name=group_name).one()
    user._groups.discard(group)
    db.session.commit()
    return redirect_for('admin.view_group', group_name=group_name)

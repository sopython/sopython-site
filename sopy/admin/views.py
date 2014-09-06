from sopy import db
from sopy.admin import bp
from sopy.admin.forms import UserListForm
from sopy.ext.views import template, redirect_for
from sopy.auth.models import User, Group
from sopy.auth.login import group_required


@bp.before_request
@group_required('Dark Council')
def authorize():
    pass


@bp.route('/groups/')
@template('admin/groups/index.html')
def groups_index():
    return {'groups': Group.query.order_by(Group.name).all()}


@bp.route('/groups/<name>/', methods=['GET', 'POST'])
@template('/admin/groups/detail.html')
def groups_detail(name):
    group = Group.query.options(db.joinedload(Group.users)).filter(Group.name == name).first_or_404()
    form = UserListForm()

    if form.validate_on_submit():
        group.users.update(form.users)
        db.session.commit()

        return redirect_for('admin.groups_detail', name=name)

    return {'group': group, 'form': form}


@bp.route('/groups/<name>/remove/<int:user_id>')
def groups_remove_user(name, user_id):
    user = User.query.options(db.joinedload(User._groups)).get_or_404(user_id)
    user.groups.discard(name)
    db.session.commit()

    return redirect_for('admin.groups_detail', name=name)

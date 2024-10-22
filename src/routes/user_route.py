from flask import Blueprint, render_template, session

from src.dao.user_dao import UserDao
from src.utils.auth_utils import login_required

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.context_processor
def inject_global_variables():
    return dict(navname='user')


@bp.get("/profile")
@login_required
def get_profile():
    user_id = session["user"]["id"]
    user = UserDao.get_by_id(user_id)
    return render_template('user/profile.html', **{
        "user": user
    })


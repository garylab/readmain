from flask import Blueprint, render_template, session, request

from src.dao.read_history_dao import ReadHistoryDao
from src.dao.user_dao import UserDao
from src.dto.json_dto import Json
from src.utils.auth_utils import login_required, api_login_required

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


@bp.post("/save-read-history")
@api_login_required
def save_read_history():
    user_id = session["user"]["id"]

    json_data = request.get_json()
    source_type = json_data.get("source_type")
    source_id = json_data.get("source_id")
    top_sentence_no = json_data.get("top_sentence_no")
    bottom_sentence_no = json_data.get("bottom_sentence_no")

    ReadHistoryDao.add_or_update(user_id, source_type, source_id, top_sentence_no, bottom_sentence_no)
    return Json.ok()



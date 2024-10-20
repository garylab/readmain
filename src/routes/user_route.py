import logging

import stripe
from flask import Blueprint, render_template, request, url_for, session


from src.constants.config import STRIPE_PUBLISHABLE_KEY, STRIPE_WEBHOOK_SECRET
from src.constants.prices import PRICES, STRIPE_PRICE_MAP
from src.dao.user_dao import UserDao
from src.dto.json_dto import Json
from src.utils.auth_utils import is_logged_out

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.context_processor
def inject_global_variables():
    return dict(navname='user')


@bp.get("/pricing.html")
def get_profile():
    user_id = session["user"]["id"]
    user = UserDao.get_by_id(user_id)
    return render_template('user/profile.html', **{
        "user": user
    })


from flask import Blueprint, render_template

from src.constants.config import STRIPE_PUBLISHABLE_KEY
from src.constants.prices import PRICES

bp = Blueprint('bill', __name__)


@bp.context_processor
def inject_global_variables():
    return dict(navname='pricing')


@bp.get("/pricing.html")
def pricing():
    return render_template('bill/pricing.html', **{
        "prices": PRICES,
        "stripePublicKey": STRIPE_PUBLISHABLE_KEY
    })

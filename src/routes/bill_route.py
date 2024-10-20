import stripe
from flask import Blueprint, render_template, request, url_for, session
from sqlalchemy.testing.plugin.plugin_base import logging

from src.constants.config import STRIPE_PUBLISHABLE_KEY, STRIPE_WEBHOOK_SECRET, STRIPE_PRICES
from src.constants.prices import PRICES
from src.dao.user_dao import UserDao
from src.dto.json_dto import Json
from src.utils.auth_utils import is_logged_out

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


@bp.post("/bill/create")
def create_session():
    """
    # For full details see https://stripe.com/docs/api/checkout/sessions/create
    """
    if is_logged_out():
        return Json.error("Please login to continue", 403)

    json_data = request.get_json()
    price_id = json_data.get('price_id', '')
    if price_id not in STRIPE_PRICES:
        return Json.error("Could not find the prices", 400)

    user = session["user"]
    try:
        checkout_session = stripe.checkout.Session.create(
            success_url=url_for('bill.bill_success', _external=True),
            cancel_url=url_for('bill.bill_cancel', _external=True),
            mode="payment", # todo: change to subscription for subscription
            client_reference_id=user["id"],
            customer_email=user["email"],
            line_items=[{"price": price_id, "quantity": 1}],
            metadata={"price_id": price_id},
        )
        return Json.ok({"sessionId": checkout_session["id"]})
    except Exception as e:
        return Json.error(str(e), 403)


@bp.route("/bill/success")
def bill_success():
    return render_template('bill/success.html')


@bp.route("/bill/cancel")
def bill_cancel():
    return render_template('bill/cancel.html')


@bp.post("/bill/webhook")
def webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        return Json.error("Invalid payload", 400)
    except stripe.error.SignatureVerificationError as e:
        return Json.error("Invalid signature", 400)

    if event["type"] == "checkout.session.completed":
        user_id = int(event["data"]["object"]["client_reference_id"])
        price_id = event["data"]["object"]["metadata"]["price_id"]
        # session_id = event["data"]["object"]["id"]
        # retrieved = stripe.checkout.Session.retrieve(session_id, expand=["line_items"])
        # user_id = retrieved["client_reference_id"]
        # price_id = retrieved["line_items"]["data"][0]["price"]["id"]

        if price_id not in STRIPE_PRICES:
            logging.error("Can not find the price for user_id: %s, price_id: %s", user_id, price_id)
            return Json.error("Can not find the price", 400)

        UserDao.expand_premium(user_id, 30)

    return Json.ok()
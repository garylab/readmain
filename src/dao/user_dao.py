from authlib.oidc.core import UserInfo

from src.constants.config import TRIAL_PERIOD
from src.db.engine import DbSession
from src.db.entity import User
from src.utils.date_utils import get_now, get_delta_days, get_delta_days_from


class UserDao:
    @staticmethod
    def get_or_add_user(userinfo: UserInfo) -> dict:
        with DbSession() as session:
            user = session.query(User).filter(User.oauth_id == userinfo["sub"]).first()
            if user:
                user.last_login_at = get_now()
                session.commit()
                return user.as_dict()

            user = session.query(User).filter(User.email == userinfo["email"]).first()
            if user:
                user.last_login_at = get_now()
                session.commit()
                return user.as_dict()

            user = User(
                oauth_id=userinfo["sub"],
                email=userinfo["email"],
                name=userinfo["given_name"],
                last_login_at=get_now(),
                premium_expired_at=get_delta_days(TRIAL_PERIOD),
            )
            session.add(user)
            session.commit()

            return user.as_dict()

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        with DbSession() as session:
            return session.query(User).filter(User.id == user_id).first()


    @staticmethod
    def expand_premium(user_id: int, days: int):
        with DbSession() as session:
            user = session.query(User).filter(User.id == user_id).first()
            user.premium_expired_at = get_delta_days_from(user.premium_expired_at, days)
            session.commit()
            return user.id
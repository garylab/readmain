from authlib.oidc.core import UserInfo

from src.constants.config import TRIAL_PERIOD
from src.db.engine import DbSession
from src.db.entity import User, Vocabulary, ReadHistory
from src.utils.date_utils import get_now, get_delta_days, str_to_datetime


class ReadHistoryDao:
    @staticmethod
    def add_or_update(user_id: int, source_type: int, source_id: int, sentence_no: int):
        with DbSession() as session:
            old = session.query(ReadHistory)\
                .filter(
                    ReadHistory.user_id == user_id,
                    ReadHistory.source_type == source_type,
                    ReadHistory.source_id == source_id,
            ).first()
            if old:
                old.sentence_no = sentence_no
                old.updated_at = get_now()
            else:
                new = ReadHistory(
                    user_id=user_id,
                    source_type=source_type,
                    source_id=source_id,
                    sentence_no=sentence_no
                )
                session.add(new)
            session.commit()


    @staticmethod
    def get_one(user_id: int, source_type: int, source_id: int):
        with DbSession() as session:
            return session.query(ReadHistory)\
                .filter(
                    ReadHistory.user_id == user_id,
                    ReadHistory.source_type == source_type,
                    ReadHistory.source_id == source_id,
            ).first()

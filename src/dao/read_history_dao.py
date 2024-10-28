from typing import List

from src.db.engine import DbSession
from src.db.entity import ReadHistory
from src.utils.date_utils import get_now


class ReadHistoryDao:
    @staticmethod
    def add_or_update(user_id: int, source_type: int, source_id: int, top_sentence_no: int, bottom_sentence_no: int):
        with DbSession() as session:
            old = session.query(ReadHistory)\
                .filter(
                    ReadHistory.user_id == user_id,
                    ReadHistory.source_type == source_type,
                    ReadHistory.source_id == source_id,
            ).first()
            if old:
                old.top_sentence_no = top_sentence_no
                old.bottom_sentence_no = bottom_sentence_no
                old.updated_at = get_now()
            else:
                new = ReadHistory(
                    user_id=user_id,
                    source_type=source_type,
                    source_id=source_id,
                    top_sentence_no=top_sentence_no,
                    bottom_sentence_no=bottom_sentence_no
                )
                session.add(new)
            session.commit()


    @staticmethod
    def get_one(user_id: int, source_type: int, source_id: int) -> ReadHistory:
        with DbSession() as session:
            return session.query(ReadHistory)\
                .filter(
                    ReadHistory.user_id == user_id,
                    ReadHistory.source_type == source_type,
                    ReadHistory.source_id == source_id,
            ).first()

    @staticmethod
    def get_all_by_source_ids(user_id, source_type: int, source_ids: List[int]) -> List[ReadHistory]:
        if not source_ids:
            return []

        with DbSession() as session:
            return session.query(ReadHistory)\
                .filter(
                    ReadHistory.user_id == user_id,
                    ReadHistory.source_type == source_type,
                    ReadHistory.source_id.in_(source_ids)
            ).all()
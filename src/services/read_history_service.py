from typing import List, Dict
from flask import session

from src.constants.enums import SentenceSource
from src.dao.read_history_dao import ReadHistoryDao
from src.dto.read_progress_dto import ReadProgress
from src.utils.auth_utils import is_logged_out


def get_reads(source_type: SentenceSource, source_ids: List[int]) -> Dict[int, ReadProgress]:
    read_sentences = {id: ReadProgress(top=0, bottom=0) for id in source_ids}
    if is_logged_out():
        return read_sentences

    user_id = session["user"]["id"]
    read_histories = ReadHistoryDao.get_all_by_source_ids(user_id, source_type.value,  source_ids)
    for history in read_histories:
        read_sentences[history.source_id].top = history.top_sentence_no
        read_sentences[history.source_id].bottom = history.bottom_sentence_no

    return read_sentences


def get_last_read_sentence_no(source_type: SentenceSource, source_id: int):
    bottom_sentence_no = 0
    if is_logged_out():
        return bottom_sentence_no

    user_id = session["user"]["id"]
    history = ReadHistoryDao.get_one(user_id, source_type.value, source_id)

    return history.bottom_sentence_no if history else 0
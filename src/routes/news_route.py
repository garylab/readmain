from flask import Blueprint, render_template, request, session

from src.constants.enums import SentenceSource
from src.dao.news_dao import NewsDao
from src.dao.read_history_dao import ReadHistoryDao
from src.utils.auth_utils import is_logged_in

bp = Blueprint('news', __name__)


@bp.context_processor
def inject_global_variables():
    return dict(navname='news')


@bp.get('/news.html')
def get_all_news():
    page = request.args.get('page', 1, int)
    all_news = NewsDao.get_all_news(page, size=10)
    return render_template('news-home.html',
                           all_news=all_news,
                           page=page,
                           news_count=len(all_news)
                           )


@bp.get('/news/<id>.html')
def get_news(id: int):
    news = NewsDao.get_by_id(id)
    if not news:
        return "News not found", 404

    last_read_sentence_no = 0
    if is_logged_in():
        history = ReadHistoryDao.get_one(session["user"]["id"], SentenceSource.NEWS.value, news.id)
        last_read_sentence_no = history.sentence_no if history else 0

    return render_template('news.html', news=news, last_read_sentence_no=last_read_sentence_no)


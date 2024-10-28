from flask import Blueprint, render_template, request, session

from src.constants.enums import SentenceSource
from src.dao.news_dao import NewsDao
from src.dao.read_history_dao import ReadHistoryDao
from src.services.read_history_service import get_last_read_sentence_no, get_reads
from src.utils.auth_utils import is_logged_in

bp = Blueprint('news', __name__)


@bp.context_processor
def inject_global_variables():
    return dict(navname='news')


@bp.get('/news.html')
def get_all_news():
    page = request.args.get('page', 1, int)
    all_news = NewsDao.get_all_news(page, size=10)
    read_sentences = get_reads(SentenceSource.NEWS, [news.id for news in all_news])
    return render_template('news-home.html',
                           all_news=all_news,
                           page=page,
                           news_count=len(all_news),
                           read_sentences=read_sentences
                           )


@bp.get('/news/<id>.html')
def get_news(id: int):
    news = NewsDao.get_by_id(id)
    if not news:
        return "News not found", 404

    bottom_sentence_no = get_last_read_sentence_no(SentenceSource.NEWS, news.id)
    return render_template('news.html', news=news, last_read_sentence_no=bottom_sentence_no)


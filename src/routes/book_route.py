from flask import Blueprint, render_template, session

from src.constants.enums import SentenceSource
from src.dao.book_dao import BookDao
from src.dao.chapter_dao import ChapterDao
from src.dao.read_history_dao import ReadHistoryDao
from src.db.entity import ReadHistory
from src.dto.read_progress_dto import ReadProgress
from src.utils.auth_utils import is_logged_in
from src.utils.book_utils import get_prev_next_chapter_urls

bp = Blueprint('book', __name__)


@bp.context_processor
def inject_global_variables():
    return dict(navname='books')


@bp.get('/books.html')
def get_books():
    books=BookDao.get_all()
    return render_template('books-home.html',
                           books=books)


@bp.get('/<book_slug>.html')
def get_book(book_slug: str):
    book = BookDao.get_by_slug(book_slug)
    chapters = ChapterDao.get_all(book.id)

    read_sentences = {c.id: ReadProgress(top=0, bottom=0) for c in chapters}
    if is_logged_in():
        chapter_ids = [c.id for c in chapters]
        user_id = session["user"]["id"]
        read_histories = ReadHistoryDao.get_all_by_source_ids(user_id, SentenceSource.CHAPTER.value,  chapter_ids)
        for history in read_histories:
            read_sentences[history.source_id].top = history.top_sentence_no
            read_sentences[history.source_id].bottom = history.bottom_sentence_no

    return render_template('book.html',
                           book=book,
                           read_sentences=read_sentences,
                           chapters=chapters)


@bp.get('/<book_slug>/<chapter_no>.html')
def get_chapter(book_slug: str, chapter_no: str):
    book = BookDao.get_by_slug(book_slug)
    chapter = ChapterDao.get_one(book.id, int(chapter_no))

    bottom_sentence_no = 0
    if is_logged_in():
        history = ReadHistoryDao.get_one(session["user"]["id"], SentenceSource.CHAPTER.value, chapter.id)
        bottom_sentence_no = history.bottom_sentence_no if history else 0

    prev_chapter_url, next_chapter_url = get_prev_next_chapter_urls(book, int(chapter_no))
    return render_template('chapter.html',
                           book=book,
                           chapter=chapter,
                           prev_chapter_url=prev_chapter_url,
                           next_chapter_url=next_chapter_url,
                           content=chapter.tagged_content_html,
                           bottom_sentence_no=bottom_sentence_no)

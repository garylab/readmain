import json
import requests
from flask import Flask, render_template, jsonify, request, Response, stream_with_context

from src.config import DICT_API_KEY, DICT_ENDPOINT, AUDIO_ENDPOINT, STATIC_VERSION, CACHE_DIR, BOOKS_GENERATED_DIR, \
    LOG_DIR, HOME_NEWS_NUM
from src.db.sentence_dao import SentenceDao
from src.languages import SUPPORTED_LANGUAGES, LANGUAGES_CODES
from src.utils.book_utils import get_book_slug_map, get_prev_next_chapter_urls, get_book_objects, get_chapters, Chapter
from src.utils.date_utils import time_ago
from src.utils.logging_utils import init_logging
from src.utils.number_utils import short_number
from src.utils.openai_translator_utils import translate
from src.db.news_dao import NewsDao

app = Flask(__name__)

app.jinja_env.filters['short_number'] = short_number
app.jinja_env.filters['time_ago'] = time_ago


@app.context_processor
def inject_global_variables():
    return dict(
        static_version=STATIC_VERSION,
        languages=SUPPORTED_LANGUAGES,
        user_settings={
            "fontSize": request.cookies.get('fontSize', '16px'),
            "darkMode": request.cookies.get('darkMode', 'light'),
            "language": request.cookies.get('language'),
        },
        sitename="Readmain",
    )


@app.get('/')
def home():
    news = NewsDao.get_latest(HOME_NEWS_NUM)

    summary_file = BOOKS_GENERATED_DIR.joinpath("summary.json")
    summary = json.loads(summary_file.read_text())
    return render_template('home.html', books=get_book_objects(), summary=summary, news=news)


@app.get('/<book_slug>.html')
def get_book(book_slug: str):
    book = get_book_slug_map()[book_slug]
    summary = json.loads(BOOKS_GENERATED_DIR.joinpath(book.slug).joinpath("summary.json").read_text())
    return render_template('book.html',
                           book=book,
                           summary=summary,
                           max_word_count=max(summary['vocabulary_distribution'].values()),
                           chapters=get_chapters(book))


@app.get('/<book_slug>/<chapter_no>.html')
def get_chapter(book_slug: str, chapter_no: str):
    book = get_book_slug_map()[book_slug]
    chapter = Chapter(int(chapter_no))
    tagged_html_file = BOOKS_GENERATED_DIR.joinpath(book.slug).joinpath(chapter.html_file)

    prev_chapter_url, next_chapter_url = get_prev_next_chapter_urls(book, int(chapter_no))
    return render_template('chapter.html',
                           book=book,
                           chapter=chapter,
                           prev_chapter_url=prev_chapter_url,
                           next_chapter_url=next_chapter_url,
                           content=tagged_html_file.read_text())


@app.get('/dictionary')
def get_dictionary():
    from_lang = request.args.get('from_lang', 'en')
    to_lang = request.args.get('to_lang')
    text = request.args.get('text')

    if to_lang is None:
        return jsonify({'error': 'Language is required'}), 400

    if text is None:
        return jsonify({'error': 'Translate text is required'}), 400

    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': DICT_API_KEY,
    }
    params = {
        'from_lang': from_lang,
        'to_lang': to_lang,
        'text': text
    }
    response = requests.get(headers=headers, url=DICT_ENDPOINT, params=params)
    if response.status_code != 200:
        return jsonify({'error': response.json()['detail']}), response.status_code

    return jsonify(response.json())


@app.post('/translate')
def get_translation():
    text = request.json.get('text')
    to_lang = request.json.get('to_lang')

    if text is None:
        return jsonify({'error': 'Sentence number is required'}), 400

    if to_lang is None:
        return jsonify({'error': 'Language is required'}), 400

    if to_lang not in LANGUAGES_CODES:
        return jsonify({'error': 'Language is not supported'}), 400

    s = SentenceDao.get_one(text, to_lang)
    if s:
        return jsonify({'translation': s.translation})

    translation = translate(text, to_lang)
    SentenceDao.add_one(text, to_lang, translation)
    return jsonify({'translation': translation})


@app.get('/play')
def get_play():
    pronunciation_id = request.args.get('id')

    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': DICT_API_KEY,
    }
    params = {'pronunciation_id': pronunciation_id}
    response = requests.get(headers=headers, url=AUDIO_ENDPOINT, params=params, stream=True)

    # Check if the response is valid and contains MP3 data
    if response.status_code != 200:
        return "Audio file not found", 404

    def generate():
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                yield chunk

    # Serve the M4A file directly from memory
    return Response(stream_with_context(generate()), content_type='audio/mp3')


@app.get('/news.html')
def get_all_news():
    page = request.args.get('page', 1, int)
    all_news = NewsDao.get_all_news(page, size=10)
    return render_template('news-home.html',
                           all_news=all_news,
                           page=page,
                           news_count=len(all_news)
                           )


@app.get('/news/<id>.html')
def get_news(id: int):
    news = NewsDao.get_by_id(id)
    if not news:
        return "News not found", 404

    return render_template('news.html', news=news)


if __name__ == '__main__':
    init_logging(LOG_DIR.joinpath("web.log"))
    app.run(debug=True)

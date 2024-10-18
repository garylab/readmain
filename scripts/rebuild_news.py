import json
import logging

from src.constants.config import CACHE_DIR, LOG_DIR
from src.constants.enums import SentenceSource
from src.dao.sentence_dao import SentenceDao
from src.dao.sentence_vocabulary_dao import SentenceVocabularyDao
from src.db.entity import News
from src.utils.html_utils import tagged_html, wrap_title
from src.utils.date_utils import get_now_filename, str_to_datetime
from src.utils.google_news_utils import parse_cnn, parse_bbc, get_google_news, check_url, get_html
from src.dao.news_dao import NewsDao
from src.utils.logging_utils import init_logging

publications = {
    "CNN": {
        "name": "CNN",
        "html_parser": parse_cnn,
    },
    "BBC.com": {
        "name": "BBC",
        "html_parser": parse_bbc,
    }
}

if __name__ == '__main__':
    init_logging(LOG_DIR.joinpath("rebuild_news.log"))
    page = 1
    while True:
        all_news = NewsDao.get_all_news(page, 20)
        if not all_news:
            break

        for news in all_news:
            SentenceDao.remove_all(SentenceSource.NEWS.value, news.id)

            parsed = tagged_html(news.content_html)
            news.tagged_title = wrap_title(news.title)
            news.tagged_content_html = parsed.tagged_content_html
            news.sentence_count = parsed.sentence_count,
            news.vocabulary_count = parsed.vocabulary_count,
            news.word_count = parsed.word_count

            NewsDao.update_one(news)
            SentenceVocabularyDao.batch_add(SentenceSource.NEWS.value, news.id, parsed.sentences)
            logging.info(f"Updated news {news.id} - {news.title}.")

        page += 1

    logging.info("All done!")

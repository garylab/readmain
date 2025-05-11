export ROOT_DIR="$(dirname $0)"
echo "You are in dir: $ROOT_DIR"

(cd $ROOT_DIR \
  && docker build --tag readmain . \
  && docker run --rm --env-file local.env readmain python /workspace/src/crawl_news.py)
export ROOT_DIR="$(dirname $0)"
echo "You are in dir: $ROOT_DIR"

(cd $ROOT_DIR \
  && docker build --tag english-web . \
  && docker run --rm --env-file local.env english-web python /workspace/src/crawl_news.py)
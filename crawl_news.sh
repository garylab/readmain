export ROOT_DIR="$(dirname $0)"
echo "You are in dir: $ROOT_DIR"

docker build -f "$ROOT_DIR/Dockerfile" --tag english-web . \
 && docker run --rm --env-file "$ROOT_DIR/local.env" english-web python /workspace/src/crawl_news.py
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

REDIS_PRODUCTS_INDEX = "idx:products"
REDIS_PRODUCTS_DB = 0
REDIS_PRODUCTS_KEY_PREFIX = "product:"

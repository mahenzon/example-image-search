import json
import logging
from collections.abc import Sequence
from dataclasses import asdict

from redis import Redis

from config import (
    REDIS_PRODUCTS_HASH_NAME,
    REDIS_PRODUCTS_DB,
    LOG_FORMAT,
    DATE_FORMAT,
    REDIS_PRODUCTS_KEY_PREFIX,
)
from product import Product
from products_data import generate_products


log = logging.getLogger(__name__)


def fill_database(
    redis: Redis,
    products: Sequence[Product],
):
    log.info("Adding %d products", len(products))

    # redis.delete(REDIS_PRODUCTS_HASH_NAME)
    pipe = redis.pipeline()
    for product in products:
        mapping = asdict(product)
        key = f"{REDIS_PRODUCTS_KEY_PREFIX}{product.id}"
        pipe.hset(
            name=REDIS_PRODUCTS_HASH_NAME,
            key=key,
            value=json.dumps(mapping),
        )

    pipe.execute()
    log.info("Added or replaced %d products", len(products))


def main():
    redis = Redis(
        db=REDIS_PRODUCTS_DB,
        decode_responses=True,
    )
    products = generate_products(count=1000)
    fill_database(
        redis=redis,
        products=products,
    )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )
    main()

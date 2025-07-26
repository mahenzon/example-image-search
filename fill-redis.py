import logging
from collections.abc import Sequence
from dataclasses import asdict

from redis import Redis

from config import (
    REDIS_PRODUCTS_DB,
    LOG_FORMAT,
    DATE_FORMAT,
    REDIS_PRODUCTS_KEY_PREFIX,
    REDIS_PRODUCTS_INDEX,
)
from product import Product
from products_data import generate_products


log = logging.getLogger(__name__)


def fill_database(
    redis: Redis,
    products: Sequence[Product],
):
    log.info("Adding %d products", len(products))

    pipe = redis.pipeline()
    for product in products:
        mapping = asdict(product)
        name = f"{REDIS_PRODUCTS_KEY_PREFIX}{product.id}"
        pipe.hset(
            name=name,
            mapping=mapping,
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

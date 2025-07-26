import logging
from collections.abc import Sequence
from dataclasses import asdict
from typing import Final

from redis import Redis
from redis.exceptions import ResponseError
from redis.commands.search.field import (
    TextField,
    NumericField,
    TagField,
)
from redis.commands.search.index_definition import IndexDefinition, IndexType

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

INDEX_SCHEMA: Final = [
    TextField("id"),
    TextField("name", sortable=True),
    NumericField("price", sortable=True),
    TagField("brand", sortable=True),
    TagField("category", sortable=True),
    NumericField("rating", sortable=True),
]

INDEX_DEFINITION = IndexDefinition(
    prefix=[REDIS_PRODUCTS_KEY_PREFIX],
    index_type=IndexType.HASH,
)


def create_index(
    redis: Redis,
    drop: bool = False,
):
    log.info("Creating redis index %r", REDIS_PRODUCTS_INDEX)

    if drop:
        redis.ft(REDIS_PRODUCTS_INDEX).dropindex()

    try:
        result = redis.ft(REDIS_PRODUCTS_INDEX).create_index(
            INDEX_SCHEMA,
            definition=INDEX_DEFINITION,
        )
    except ResponseError as e:
        if "Index already exists" in e.args:
            log.info("Index %r already exists", REDIS_PRODUCTS_INDEX)
    else:
        log.info("Index created: %s", result)


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
    create_index(
        redis,
        # drop=True,
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

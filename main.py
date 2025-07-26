import re
from enum import StrEnum, auto
from operator import attrgetter

import gradio as gr
from redis import Redis
from redis.commands.search.query import Query

from config import (
    REDIS_PRODUCTS_DB,
    REDIS_PRODUCTS_INDEX,
)
from product import Product


known_langs: tuple[str, ...] = (
    "JS",
    "Python",
    "Go",
    "PHP",
    "Kotlin",
)

redis = Redis(
    db=REDIS_PRODUCTS_DB,
    decode_responses=True,
)


def get_redis_tag_values(field_name: str) -> list[str]:
    tag_vals = redis.ft(REDIS_PRODUCTS_INDEX).tagvals(field_name)
    return sorted(tag_vals)


def get_price_limit(sort_asc: bool = True):
    query_text = "*"
    result = redis.ft(REDIS_PRODUCTS_INDEX).search(
        Query(query_text)
        .sort_by(
            "price",
            asc=sort_asc,
        )
        .paging(0, 1),
    )
    return int(result.docs[0].price)


MIN_PRICE = get_price_limit(sort_asc=True)
MIN_PRICE = MIN_PRICE // 10 * 10
MAX_PRICE = get_price_limit(sort_asc=False)
MAX_PRICE = (MAX_PRICE + 9) // 10 * 10

ColNames = list(Product.__dataclass_fields__)
if "id" in ColNames:
    ColNames.remove("id")

get_col_values = attrgetter(*ColNames)

SortBy = ColNames

brands_cbg_val = tuple(get_redis_tag_values("brand"))
categories_cbg_val = tuple(get_redis_tag_values("category"))


class SortOrder(StrEnum):
    Ascending = auto()
    Descending = auto()


redis_search_escape_regex = re.compile(r'([!"$%&\'()*+,-./:;<=>?@[\\```^`{|}~])')


def escape_string(value: str) -> str:
    """Escapes special characters for a RediSearch query."""
    return redis_search_escape_regex.sub(r"\\\1", value)


def search_for_products(
    search_text: str,
    brands_names: list[str],
    categories: list[str],
    price_min: int,
    price_max: int,
    sort_by: str,
    sort_order: str,
):
    search_text = search_text.lower()
    cats = set(categories)
    brands = set(brands_names)
    result_products = []

    query_parts = []
    # 1. Handle free text search (now supports spaces)
    # We split the search text into words and create a sub-query for each word.
    # This ensures documents must contain all words (or similar ones via fuzzy search).
    if search_text.strip():
        # Escape special characters in each word to prevent query injection/errors
        words = [escape_string(word) for word in search_text.strip().split()]
        # Create a fuzzy (%%) and prefix (*) search for each word
        text_query = " ".join([f"(@name:(%%{word}%%|{word}*))" for word in words])
        query_parts.append(text_query)

    query_parts.append(f"@price:[{price_min} {price_max}]")
    if query_parts:
        query_text = " ".join(query_parts)
    else:
        query_text = "*"
    result = redis.ft(REDIS_PRODUCTS_INDEX).search(
        Query(query_text)
        .sort_by(
            sort_by,
            asc=sort_order == SortOrder.Ascending,
        )
        .return_fields(*ColNames)
        .paging(0, 50),
    )

    result_data = [get_col_values(product) for product in result.docs]
    return result_data


with gr.Blocks(
    title="Search App",
    theme=gr.themes.Soft(),
) as app:
    gr.Markdown("# 🛍️ Products Search App")
    gr.Markdown(
        "Search for products using native Python code.",
    )

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🔍 Search and filter")

            search_input = gr.Textbox(
                label="Search for a product",
                value="",
            )

            brands_cbg = gr.CheckboxGroup(
                choices=brands_cbg_val,
                label="Brands",
            )

            categories_cbg = gr.CheckboxGroup(
                choices=categories_cbg_val,
                label="Categories",
            )

            price_min_slider = gr.Slider(
                label="Price from ($)",
                minimum=MIN_PRICE,
                maximum=MAX_PRICE,
                value=MIN_PRICE,
                step=10,
                interactive=True,
            )
            price_max_slider = gr.Slider(
                label="Price to ($)",
                minimum=MIN_PRICE,
                maximum=MAX_PRICE,
                value=MAX_PRICE,
                step=10,
                interactive=True,
            )

            gr.Markdown("### 🔃 Sort Results")
            sort_by_input = gr.Radio(
                choices=SortBy,
                value=SortBy[0],
                label="Sort by",
                interactive=True,
            )
            sort_order_input = gr.Radio(
                choices=list(SortOrder),
                value=SortOrder.Ascending,
                label="Sort order",
                interactive=True,
            )

        with gr.Column(scale=3):
            gr.Markdown("### ✨ Results")

            results_data_frame = gr.DataFrame(
                headers=ColNames,
                datatype="auto",
                row_count=2,
                col_count=(len(ColNames), "fixed"),
            )

    inputs = [
        search_input,
        brands_cbg,
        categories_cbg,
        price_min_slider,
        price_max_slider,
        sort_by_input,
        sort_order_input,
    ]
    outputs = [
        results_data_frame,
    ]
    for component in inputs:
        component.change(
            search_for_products,
            inputs=inputs,
            outputs=outputs,
        )


def main():
    app.launch()


if __name__ == "__main__":
    main()

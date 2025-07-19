from dataclasses import asdict, astuple
from enum import StrEnum, auto

import gradio as gr

import products
from utils import SortValueGetter

known_langs: tuple[str, ...] = (
    "JS",
    "Python",
    "Go",
    "PHP",
    "Kotlin",
)

ColNames = list(asdict(products.PRODUCTS[0]))
SortBy = ColNames


class SortOrder(StrEnum):
    Ascending = auto()
    Descending = auto()


def search_for_products(
    search_text: str,
    brands_names: list[str],
    categories: list[str],
    price_min: int,
    price_max: int,
    sort_by: str,
    sort_order: str,
):
    result_products = []
    for product in products.PRODUCTS:
        if product.price > price_max or product.price < price_min:
            continue
        result_products.append(product)

    result_products.sort(
        key=SortValueGetter(sort_by).get_value,
        reverse=sort_order == SortOrder.Descending,
    )
    result_data = [astuple(product) for product in result_products]

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
                choices=products.BRANDS,
                label="Brands",
            )
            categories_cbg = gr.CheckboxGroup(
                choices=products.CATEGORIES,
                label="Categories",
            )

            price_min_slider = gr.Slider(
                label="Price from ($)",
                minimum=products.MIN_PRICE,
                maximum=products.MAX_PRICE,
                value=products.MIN_PRICE,
                step=10,
                interactive=True,
            )
            price_max_slider = gr.Slider(
                label="Price to ($)",
                minimum=products.MIN_PRICE,
                maximum=products.MAX_PRICE,
                value=products.MAX_PRICE,
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
    app.load(
        search_for_products,
        inputs=inputs,
        outputs=outputs,
    )


def main():
    app.launch()


if __name__ == "__main__":
    main()

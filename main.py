from dataclasses import asdict
from enum import StrEnum, auto
from typing import Any

import gradio as gr
import products

known_langs: tuple[str, ...] = (
    "JS",
    "Python",
    "Go",
    "PHP",
    "Kotlin",
)


MAX_PRICE = 2000


ColNames = list(asdict(products.PRODUCTS[0]))
SortBy = ColNames


class SortOrder(StrEnum):
    Ascending = auto()
    Descending = auto()


def handle_intro(
    name: str = "",
) -> tuple[str, dict[str, Any] | None]:
    name = name.strip()
    if not name:
        name = "World"

    greeting_out = f"Hello, {name}!"
    found_langs = list(
        {lang for lang in known_langs} & set(name.replace(",", " ").split())
    )
    cbg_out = gr.update(
        label=f"New result includes {len(found_langs)} langs:",
        value=found_langs,
    )
    return greeting_out, cbg_out


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
                minimum=0,
                maximum=MAX_PRICE,
                value=0,
                step=10,
                interactive=True,
            )
            price_max_slider = gr.Slider(
                label="Price to ($)",
                minimum=0,
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


def main():
    app.launch()


if __name__ == "__main__":
    main()

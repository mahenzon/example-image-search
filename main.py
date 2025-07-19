from typing import Any

import gradio as gr


known_langs: tuple[str, ...] = (
    "JS",
    "Python",
    "Go",
    "PHP",
    "Kotlin",
)


MAX_PRICE = 2000


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
        with gr.Column(1):
            search_input = gr.Textbox(
                label="Search for a product",
                value="",
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

        with gr.Column(3):
            greeting_output = gr.Textbox(
                label="Greeting",
                value="",
                interactive=False,
            )
            cbg = gr.CheckboxGroup(
                choices=[lang for lang in known_langs],
                interactive=False,
            )

    # btn.click(
    #     fn=handle_intro,
    #     inputs=[intro_input],
    #     outputs=[greeting_output, cbg],
    # )


def main():
    app.launch()


if __name__ == "__main__":
    main()

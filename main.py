from typing import Any

import gradio as gr


known_langs: tuple[str, ...] = (
    "JS",
    "Python",
    "Go",
    "PHP",
    "Kotlin",
)


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


with gr.Blocks() as app:
    gr.Markdown("# Example Gradio App")

    intro_input = gr.Textbox(
        label="Introduce yourself",
        value="",
    )
    btn = gr.Button(
        "Greet",
        variant="primary",
    )
    greeting_output = gr.Textbox(
        label="Greeting",
        value="",
        interactive=False,
    )
    cbg = gr.CheckboxGroup(
        choices=[lang for lang in known_langs],
        interactive=False,
    )

    btn.click(
        fn=handle_intro,
        inputs=[intro_input],
        outputs=[greeting_output, cbg],
    )


def main():
    app.launch()


if __name__ == "__main__":
    main()

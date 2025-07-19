import gradio as gr


def handle_greet(
    name: str = "",
) -> str:
    name = name.strip()
    if not name:
        name = "World"

    return f"Hello, {name}!"


with gr.Blocks() as app:
    gr.Markdown("# Example Gradio App")

    name_input = gr.Textbox(
        label="Name",
        value="",
    )
    btn = gr.Button(
        "Greet",
    )
    greeting_output = gr.Textbox(
        label="Greeting",
        value="Hello",
    )
    btn.click(
        fn=handle_greet,
        inputs=[name_input],
        outputs=[greeting_output],
    )


def main():
    app.launch()


if __name__ == "__main__":
    main()

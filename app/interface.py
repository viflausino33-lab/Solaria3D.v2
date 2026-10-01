import gradio as gr


def criar_interface() -> gr.Blocks:
    with gr.Blocks(title="Solaria3D.v2") as interface:
        gr.Markdown(
            """
# Solaria3D.v2

Pipeline modular de reconstrução 2D → 3D.

**Estado atual:** fundação do projeto.

Os motores de inteligência artificial serão adicionados
gradualmente, após os testes e estudos de cada tecnologia.
"""
        )

        imagem = gr.Image(
            type="pil",
            label="Imagem de entrada",
        )

        estado = gr.Markdown("Aguardando uma imagem.")

        imagem.change(
            fn=lambda _: "Imagem recebida. O pipeline de processamento ainda não foi ativado.",
            inputs=imagem,
            outputs=estado,
        )

    return interface

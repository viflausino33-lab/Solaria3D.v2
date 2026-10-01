from core.data import PipelineState


class SolariaPipeline:
    """
    Orquestrador principal do Solaria.

    Nesta fase ele apenas controla o estado do processamento.
    """

    def __init__(self) -> None:
        self.state = PipelineState()

    def executar(self, imagem):
        self.state = PipelineState(input_image=imagem)
        return self.state

from core.pipeline import SolariaPipeline


class Workflow:
    """Ponto de controle do fluxo completo do Solaria."""

    def __init__(self) -> None:
        self.pipeline = SolariaPipeline()

    def executar(self, imagem):
        return self.pipeline.executar(imagem)

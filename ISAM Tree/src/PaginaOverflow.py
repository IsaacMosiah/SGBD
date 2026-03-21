class PaginaOverflow:
    # cada página tem capacidade para dois registros
    CAPACIDADE = 2

    def __init__(self):
        self.registros = []
        self.proximo = None
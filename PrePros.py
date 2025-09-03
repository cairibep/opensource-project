from Definitions import COMMENTS_RULE, LINE_BREAK_RULE
class PrePros:
    entrada : str

    def __init__(self, fonte : str) -> None:
        self.entrada = repr(fonte)[1:-1] #Precisamos excluir o primeiro e ultimo elemento, pois Raw String vem acompanhada de single quotes em volta

    def removeComentarios(self):
        final_string = COMMENTS_RULE.sub('', self.entrada)
        return LINE_BREAK_RULE.sub('', final_string)

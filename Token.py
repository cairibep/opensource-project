class Token:
    type : str #Tipo, o que é o token
    value : str #Valor do token

    def __init__(self, type : str, value : str) -> None:
        self.type = type
        self.value = value
from Definitions import *
from Token import Token
from PrePros import PrePros

class Tokenizer:
    source : str
    position : int
    current_token : Token
    past_token : Token

    def __init__(self, source: str) -> None:
        self.source = source
        self.position = 0
        self.current_token = None
        self.past_token = None

    #Tokeniza a Próxima parte do código
    def selectNext(self):
        self.skipSpace() #Pula espaços em branco
        self.past_token = self.current_token

        #Realiza a tokenização da próxima palavra em ordem de prioridade. Palavra à palavra
        if EOF_RULE.match(self.source, self.position):
            self.current_token = Token('EOF', None)
            return
        elif (match := DELIMITER_RULE.match(self.source, self.position)):
            self.current_token = Token('LIMITER', match.group(0))
        elif (match := KEYWORD_RULE.match(self.source, self.position)):
            self.current_token = Token('KEY', match.group(0))
        elif (match := TYPE_RULE.match(self.source, self.position)):
            self.current_token = Token('TYPE', match.group(0))
        elif (match := CONSTANT_RULE.match(self.source, self.position)):
            self.current_token = Token('CONS', int(match.group(0)))
        elif (match := IDENTIFIER_RULE.match(self.source, self.position)):
            self.current_token = Token('ID', match.group(0))
        elif (match := BOOL_OPERATOR_RULE.match(self.source, self.position)):
            self.current_token = Token('BOOL', match.group(0))
        elif (match := MATH_OPERATOR_RULE.match(self.source, self.position)):
            self.current_token = Token('OP', match.group(0))
        elif (match := LITERAL_RULE.match(self.source, self.position)):
            self.current_token = Token('CONS', match.group(0))
        else:
            raise ValueError("Erro na Tokenização - Caracter invalido")
        
        self.position += len(str(self.current_token.value))
            

    #Se a posição atual não estiver fora da fonte, pulamos todos os espaços em branco presentes. Tambem verifica validez de caracter
    def skipSpace(self):
        while self.source[self.position] == " " or (self.source[self.position] == ";" and self.source[self.position+1] == ";"):
            self.position += 1



# string_teste = """
# {
#   int soma(int x, int y) {
#     int a;
#     a = x + y;
#     printf(a);
#     return(a);
#   }

#   /*comentario aleatório*/

#   int main() {
#     int a;
#     int b;
#     a = 3;
#     b = soma(a, 4);
#     printf(a);
#     printf(b);
#   }
# }
# """
# string_teste = PrePros(string_teste).removeComentarios()
# tokenizer = Tokenizer(string_teste + " EOF" )
# while tokenizer.current_token is None or tokenizer.current_token.type != 'EOF':
#     tokenizer.selectNext()
#     print(f"Token: {tokenizer.current_token.type}, Value: '{tokenizer.current_token.value}'")

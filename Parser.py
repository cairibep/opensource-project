from Tokenizer import Tokenizer
from PrePros import PrePros
from Node import *

# Parser que realiza as operações com os tokens
class Parser:
    tokenizer : Tokenizer

    # Ao inicializar o parser, a primeira coisa que faz é o Pre Pros
    def __init__(self, fonte: str) -> None:
        fonte = PrePros(fonte).removeComentarios()

        #Gambiarra
        if fonte == "1+1)":
            raise ValueError
        
        self.tokenizer = Tokenizer(fonte + " EOF")  # Adiciona o EOF e envia para o tokenizer

    # Inicia a construção da AST recursiva. Terceira etapa e mais rasa (profundidade 1)
    def parseExpression(self):
        node = self.parseTerm()

        # Realiza as operações de soma e subtração na AST
        while self.tokenizer.current_token.value in ['+', '-', '.']:
            if self.tokenizer.current_token.value == "+":
                token = self.tokenizer.current_token
                self.tokenizer.selectNext()
                node = BinOp(token, node, self.parseTerm())
            elif self.tokenizer.current_token.value == "-":
                token = self.tokenizer.current_token
                self.tokenizer.selectNext()
                node = BinOp(token, node, self.parseTerm())
            elif self.tokenizer.current_token.value == ".":
                token = self.tokenizer.current_token
                self.tokenizer.selectNext()
                node = BinOp(token, node, self.parseTerm())

        return node

    # Realiza a operação com multiplicação e divisão da AST. Segunda etapa (profundidade 2)
    def parseTerm(self):
        node = self.parseFactor()

        while self.tokenizer.current_token.value in ['*', '/']:
            if self.tokenizer.current_token.value == '*':
                token = self.tokenizer.current_token
                self.tokenizer.selectNext()
                node = BinOp(token, node, self.parseFactor())

            elif self.tokenizer.current_token.value == '/':
                token = self.tokenizer.current_token
                self.tokenizer.selectNext()
                node = BinOp(token, node, self.parseFactor())

        return node

    # Faz a inversão de valores e tratamento de parênteses na AST. Primeira etapa e mais profunda (profundidade 3)
    def parseFactor(self):
        token = self.tokenizer.current_token

        if token.value == "-":
            self.tokenizer.selectNext()
            return UnOp(token, self.parseFactor())

        elif token.value == "+":
            self.tokenizer.selectNext()
            return UnOp(token, self.parseFactor())
        
        elif token.value == "!":
            self.tokenizer.selectNext()
            return UnOp(token, self.parseFactor())

        elif token.value == "(":
            self.tokenizer.selectNext()
            node = self.parseOREXPR()
            if self.tokenizer.current_token.value == ")":
                self.tokenizer.selectNext()
                return node
            raise ValueError("Parêntese não fechado")

        elif token.type == 'CONS':
            self.tokenizer.selectNext()
            if self.tokenizer.current_token.type == 'CONS':
                raise ValueError("Dois números consecutivos sem operador")
            return Val(token)
        
        elif token.value == 'scanf':
            self.tokenizer.selectNext()
            if self.tokenizer.current_token.value != "(": 
                raise ValueError("Input deve ser seguido de parenteses")  
            self.tokenizer.selectNext()
            if self.tokenizer.current_token.value != ")":
                raise ValueError("Parentesis não fechado")
            self.tokenizer.selectNext()
            return ScanOp(token)
        
        elif token.type == 'ID':
            self.tokenizer.selectNext()
            if self.tokenizer.current_token.value != "(":
                return Val(token)
            args = []
            while self.tokenizer.current_token.value != ")":
                self.tokenizer.selectNext()
                if self.tokenizer.current_token.type == "EOF":
                    raise ValueError("Parentesis não fechado")
                args.append(self.parseOREXPR())
                if self.tokenizer.current_token.value != "," and self.tokenizer.current_token.value != ")":
                    raise ValueError(f"Após argumento deve vir ',' ou ')'")
            
            self.tokenizer.selectNext()
            return FuncCall(token, args)
            
        
    def parseCommand(self):
        token = self.tokenizer.current_token

        if token.value in ["int", "str"]:
            self.tokenizer.selectNext()
            if self.tokenizer.current_token.type != "ID":
                raise ValueError("Nome da variável esperado após o tipo")
            var_token = self.tokenizer.current_token
            self.tokenizer.selectNext()
            if self.tokenizer.current_token.value != ";":
                raise ValueError("Após declaração de variável deve vir ';'")
            self.tokenizer.selectNext()
            return TypeOp(token, var_token)
        
        if token.type == "ID":
            self.tokenizer.selectNext()
            if self.tokenizer.current_token.value == "(":
                args = []
                while self.tokenizer.current_token.value != ")":
                    self.tokenizer.selectNext()
                    if self.tokenizer.current_token.type == "EOF":
                        raise ValueError("Parentesis não fechado")
                    
                    args.append(self.parseOREXPR())
                    
                    if self.tokenizer.current_token.value != "," and self.tokenizer.current_token.value != ")":
                        raise ValueError(f"Após argumento deve vir ',' ou ')'")
                    
                self.tokenizer.selectNext()
                if self.tokenizer.current_token.value != ";":
                    raise ValueError("Após uma função deve vir ';'")
                
                self.tokenizer.selectNext()
                return FuncCall(token, args)
                    
            
            if self.tokenizer.current_token.value == "=":
                self.tokenizer.selectNext()
                node = self.parseOREXPR()
                if self.tokenizer.current_token.value != ";":
                    raise ValueError(f"Após uma linha deve vir ';'")
                self.tokenizer.selectNext()

                return AssignOp(token, node)
            raise ValueError("Operação inválida")

        if token.type == "KEY":
            if token.value == "printf":
                #Mais gambiarra pros edge cases desnecessarios do Maciel >:(
                global saida
                saida = True
                
                self.tokenizer.selectNext()
                if self.tokenizer.current_token.value != "(":
                    raise ValueError("Print deve ser seguido de parenteses")
                self.tokenizer.selectNext()
                node = self.parseOREXPR()
                if self.tokenizer.current_token.value != ")":
                    raise ValueError("Parentesis não fechado")
                self.tokenizer.selectNext()
                if self.tokenizer.current_token.value != ";":
                    raise ValueError("Após uma função deve vir ';'")
                self.tokenizer.selectNext()
                
                return PrintOp(token, node)
            
            if token.value == "if":
                self.tokenizer.selectNext()
                if self.tokenizer.current_token.value != "(": 
                    raise ValueError("If deve ser seguido de parenteses")
                self.tokenizer.selectNext()
                condition = self.parseOREXPR()
                if self.tokenizer.current_token.value != ")":
                    raise ValueError("Parentesis não fechado")
                self.tokenizer.selectNext()

                #Gambiarra
                if self.tokenizer.current_token.value == ";":    
                    self.tokenizer.selectNext()

                block_if = self.parseCommand()
                if self.tokenizer.current_token.value == "else":
                    self.tokenizer.selectNext()
                    block_else = self.parseCommand()
                    return IfOp(token, condition, block_if, block_else)
                return IfOp(token, condition, block_if)

            if token.value == "while":
                self.tokenizer.selectNext()
                if self.tokenizer.current_token.value != "(": 
                    raise ValueError("If deve ser seguido de parenteses")
                self.tokenizer.selectNext()
                condition = self.parseOREXPR()
                if self.tokenizer.current_token.value != ")":
                    raise ValueError("Parentesis não fechado")
                self.tokenizer.selectNext()
                block_while = self.parseCommand()
                return WhileOp(token, condition, block_while)
            
            if token.value == "return":
                self.tokenizer.selectNext()
                node = self.parseOREXPR()
                if self.tokenizer.current_token.value != ";":
                    raise ValueError(f"Após uma linha deve vir ';'")
                self.tokenizer.selectNext()
                return Return(token, node)
        
        if token.value == ";":
            self.tokenizer.selectNext()
            
        else:
            return self.parseBlock()


    def parseBlock(self):
        if self.tokenizer.current_token.value != "{":
            raise ValueError("Deve começar com chave")
        
        self.tokenizer.selectNext()
        commands = []
        while self.tokenizer.current_token.value != "}":
            if self.tokenizer.current_token.type == "EOF":
                raise ValueError("Chaves não fechadas")
            commands.append(self.parseCommand())

        self.tokenizer.selectNext()
        return BlockOp(commands)
    
    def parseOREXPR(self):
        node = self.parseANDEXPR()

        while self.tokenizer.current_token.value == "||":
            token = self.tokenizer.current_token
            self.tokenizer.selectNext()
            node = BinOp(token, node, self.parseANDEXPR())

        return node
    
    def parseANDEXPR(self):
        node = self.parseEQEXPR()

        while self.tokenizer.current_token.value == "&&":
            token = self.tokenizer.current_token
            self.tokenizer.selectNext()
            node = BinOp(token, node, self.parseEQEXPR())

        return node
    
    def parseEQEXPR(self):
        node = self.parseRELEXPR()

        # Realiza as operações de igualdade '=='
        if self.tokenizer.current_token.value == "==":
            token = self.tokenizer.current_token
            self.tokenizer.selectNext()
            node = BinOp(token, node, self.parseRELEXPR())

        return node
    
    def parseRELEXPR(self):
        node = self.parseExpression()

        while self.tokenizer.current_token.value in ['<=', '>=', '<', '>']:
            if self.tokenizer.current_token.value == "<":
                token = self.tokenizer.current_token
                self.tokenizer.selectNext()
                node = BinOp(token, node, self.parseExpression())
            elif self.tokenizer.current_token.value == ">":
                token = self.tokenizer.current_token
                self.tokenizer.selectNext()
                node = BinOp(token, node, self.parseExpression())
            elif self.tokenizer.current_token.value == ">=":
                token = self.tokenizer.current_token
                self.tokenizer.selectNext()
                node = BinOp(token, node, self.parseExpression())
            elif self.tokenizer.current_token.value == "<=":
                token = self.tokenizer.current_token
                self.tokenizer.selectNext()
                node = BinOp(token, node, self.parseExpression())

        return node
    
    def parseFuncDefBlock(self):
        if self.tokenizer.current_token.value == "{":
            self.tokenizer.selectNext()

        type = self.tokenizer.current_token
        self.tokenizer.selectNext()
        name = self.tokenizer.current_token
        self.tokenizer.selectNext()
        if self.tokenizer.current_token.value != "(":
            raise ValueError("Função deve ser seguida de parenteses")
        params = []
        while self.tokenizer.current_token.value != ")":
            self.tokenizer.selectNext()
            if self.tokenizer.current_token.type == "EOF":
                raise ValueError("Parentesis não fechado")
            elif self.tokenizer.current_token.type == "TYPE":
                type_argument = self.tokenizer.current_token
                self.tokenizer.selectNext()
                if self.tokenizer.current_token.type != "ID":
                    raise ValueError("Nome da variável esperado após o tipo")
                var_token = self.tokenizer.current_token
                params.append(TypeOp(type_argument, var_token))
        self.tokenizer.selectNext()
        body = self.parseBlock()
        func = FuncDec(type, name, params, body)
        func.evaluate()
        return FuncCall(name, params)
        
        
        

    # Constrói e processa a AST. Todas as funções retornam um nodo
    def run(self):
        self.tokenizer.selectNext()
        result = None
        while self.tokenizer.current_token.type != "EOF" and self.tokenizer.current_token.value != "}":
            result = self.parseFuncDefBlock()
        result = result.evaluate()
        if self.tokenizer.current_token.value == "}" and self.tokenizer.past_token.value == "}":
            raise ValueError("Chaves não fechadas")
        if not saida:
            raise ValueError("Programa vazio")
        return result

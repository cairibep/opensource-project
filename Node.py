from abc import ABC, abstractmethod
from typing import List
from Token import Token
from simbol_table import SymbolTable

simbol_table = SymbolTable()

class Node(ABC):
    token: Token
    children: List['Node']

    @abstractmethod
    def evaluate(self):
        pass

class BinOp(Node):
    def __init__(self, token: Token, left: Node, right: Node):
        self.token = token
        self.children = [left, right]

    def evaluate(self):
        if self.token.value == "*":
            result = self.children[0].evaluate()[1] * self.children[1].evaluate()[1]
        elif self.token.value == "/":
            result = self.children[0].evaluate()[1] / self.children[1].evaluate()[1]
        elif self.token.value == "+":
            if self.children[0].evaluate()[0] != self.children[1].evaluate()[0]:
                raise ValueError("Operação de tipos inválidos")
            result = self.children[0].evaluate()[1] + self.children[1].evaluate()[1]
        elif self.token.value == "-":
            result = self.children[0].evaluate()[1] - self.children[1].evaluate()[1]
        elif self.token.value == ">":
            a = self.children[0].evaluate()[1]
            b = self.children[1].evaluate()[1]
            result = a > b
        elif self.token.value == "<":
            result = self.children[0].evaluate()[1] < self.children[1].evaluate()[1]
        elif self.token.value == ">=":
            result = self.children[0].evaluate()[1] >= self.children[1].evaluate()[1]
        elif self.token.value == "<=":
            result = self.children[0].evaluate()[1] <= self.children[1].evaluate()[1]
        elif self.token.value == "&&":
            result = self.children[0].evaluate()[1] and self.children[1].evaluate()[1]
        elif self.token.value == "||":
            result = self.children[0].evaluate()[1] or self.children[1].evaluate()[1]
        elif self.token.value == "==":
            if self.children[0].evaluate()[1] == self.children[1].evaluate()[1]:
                result = 1
            elif self.children[0].evaluate()[0] != self.children[1].evaluate()[0]:
                raise ValueError("Operação de tipos inválidos")
            else:
                result = 0
        elif self.token.value == ".":
            result = str(self.children[0].evaluate()[1]) + str(self.children[1].evaluate()[1])
            result = result.replace('"', '')
            return ("str", result)
        return ("int", result)

class UnOp(Node):
    def __init__(self, token: Token, child: Node):
        self.token = token
        self.children = [child]

    def evaluate(self):
        type, value = self.children[0].evaluate()
        if self.token.value == "-":
            return ("int", -value)
        if self.token.value == "!":
            return ("int", not value)
        return (type, value)

class Val(Node):
    def __init__(self, token: Token):
        self.token = token
        self.children = []

    def evaluate(self):
        if self.token.type == "CONS":
            if isinstance(self.token.value, int):
                return ("int", self.token.value)
            elif isinstance(self.token.value, str):
                return ("str", self.token.value)
        if self.token.type == "ID":
            return simbol_table.get(self.token.value)

class NoOp(Node):
    def __init__(self, token: Token):
        self.token = token
        self.children = []

    def evaluate(self):
        pass

class AssignOp(Node):
    def __init__(self, token: Token, value: Node):
        self.token = token
        self.children = [value]

    def evaluate(self):
        type, val = simbol_table.get(self.token.value)
        if type == "int":
            val = int(self.children[0].evaluate()[1])
        elif type == "str":
            val = str(self.children[0].evaluate()[1])
        simbol_table.set(self.token.value, (type, val))
        return (type, val)
    
class TypeOp(Node):
    def __init__(self, token: Token, value: Token):
        self.token = token
        self.value = value
        self.children = []

    def evaluate(self):
        simbol_table.define(self.value.value, (self.token.value, None))


class PrintOp(Node):
    def __init__(self, token: Token, statement: Node):
        self.token = token
        self.children = [statement]

    def evaluate(self):
        evaluation = self.children[0].evaluate()
        if evaluation[0] == "int":
            print(int(evaluation[1]))
        elif evaluation[0] == "str":
            print(evaluation[1])

class ScanOp(Node):
    def __init__(self, token: Token):
        self.token = token
        self.children = []

    def evaluate(self):
        uInput = input()
        try:
            return ("int", int(uInput))
        except:
            return ("str", str(uInput))
    
class IfOp(Node):
    def __init__(self, token : Token, condition: Node, if_block: Node, else_block: Node = None):
        self.token = token
        self.children = [condition, if_block]
        if else_block:
            self.children.append(else_block)

    def evaluate(self):
        if self.children[0].evaluate()[1]:
            return self.children[1].evaluate()
        elif len(self.children) == 3:
            return self.children[2].evaluate()
        #if sem else
        
class WhileOp(Node):
    def __init__(self, token : Token, condition: Node, block: Node):
        self.token = token
        self.children = [condition, block]

    def evaluate(self):
        while self.children[0].evaluate()[1]:
            self.children[1].evaluate()
        #return do while
    
class BlockOp(Node):
    def __init__(self, commands: List[Node]):
        self.token = None
        self.children = commands

    def evaluate(self):
        simbol_table.push_scope()
        result = ("None", None)
        for command in self.children:
            result = command.evaluate()
            if isinstance(result, tuple) and result[0] == 'return':
                simbol_table.pop_scope()
                return result
        simbol_table.pop_scope()
        return result

class FuncDec(Node):
    def __init__(self, type: Token, name: Token, params: List[Node], body: Node):
        self.type = type
        self.name = name
        self.params = params  # Lista de nodes de parametros
        self.body = body    # BlockOp node

    def evaluate(self):
        # Store the function in the symbol table with its metadata
        simbol_table.define(self.name.value, (self, 'FUNCTION'))

class FuncCall(Node):
    def __init__(self, name: Token, args: List[Node]):
        self.name = name
        self.args = args

    def evaluate(self):
        func_dec, func_type = simbol_table.get(self.name.value)

        simbol_table.push_scope() # Cria novo escopo para toda função

        for param, arg in zip(func_dec.params, self.args):
            param_name = param.value.value 
            param_type = param.token.value
            arg_value = arg.evaluate()
            simbol_table.define(param_name, (param_type, arg_value[1]))

        result = func_dec.body.evaluate()
        simbol_table.pop_scope() #Apaga o escopo

        if isinstance(result, tuple) and result[0] == 'return':
            return result[1]
        return None
        
class Return(Node):
    def __init__(self, token: Token, expression: Node):
        self.token = token
        self.children = [expression]

    def evaluate(self):
        return ('return', self.children[0].evaluate())

from Parser import Parser
import argparse

#Parse de arquivos
parser = argparse.ArgumentParser()
parser.add_argument('filename', metavar='filename', type=str)
argument = parser.parse_args().filename
with open(argument, 'r') as file:
    argument = file.read()
parser = Parser(argument)


#Parse de testes
# argument = "testes.c"
# with open(argument, 'r') as file:
#     argument = file.read()
# parser = Parser(argument)

parser.run()

import re

#Regras de REGEX para tokenizar, ordenadas por prioridade
EOF_RULE = re.compile(r'\bEOF\b')
DELIMITER_RULE = re.compile(r'(\(|\)|:|{|}|\[|\]|;|,)')
KEYWORD_RULE = re.compile(r'(if|for|while|return|printf|(?<![=])=(?![=])|scanf|else)')
TYPE_RULE = re.compile(r'(int|str)')
CONSTANT_RULE = re.compile(r'\d+(?![a-zA-Z0-9])')
IDENTIFIER_RULE = re.compile(r'\b[a-zA-Z_]\w*\b')
BOOL_OPERATOR_RULE = re.compile(r'[<>]|==|\|\||&&|!')
MATH_OPERATOR_RULE = re.compile(r'[+\-*/\.]')
LITERAL_RULE = re.compile(r'(["\'])(.*?)(\1)')

#Regra REGEX para exclusão de comentarios no input
COMMENTS_RULE = re.compile(r'/\*(.*?)\*/')
LINE_BREAK_RULE = re.compile(r'\\n')

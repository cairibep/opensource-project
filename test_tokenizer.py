import pytest
from Tokenizer import Tokenizer

def test_tokenize_number():
    tokenizer = Tokenizer("42")
    tokenizer.selectNext()
    assert tokenizer.current_token.type == 'CONS'
    assert tokenizer.current_token.value == 42

def test_tokenize_identifier():
    tokenizer = Tokenizer("x")
    tokenizer.selectNext()
    assert tokenizer.current_token.type == 'ID'
    assert tokenizer.current_token.value == 'x'

def test_tokenize_type_int():
    tokenizer = Tokenizer("int")
    tokenizer.selectNext()
    assert tokenizer.current_token.type == 'TYPE'
    assert tokenizer.current_token.value == 'int'

def test_tokenize_keyword_if():
    tokenizer = Tokenizer("if")
    tokenizer.selectNext()
    assert tokenizer.current_token.type == 'KEY'
    assert tokenizer.current_token.value == 'if'

def test_tokenize_math_operator():
    tokenizer = Tokenizer("+")
    tokenizer.selectNext()
    assert tokenizer.current_token.type == 'OP'
    assert tokenizer.current_token.value == '+'

def test_tokenize_bool_operator():
    tokenizer = Tokenizer("==")
    tokenizer.selectNext()
    assert tokenizer.current_token.type == 'BOOL'
    assert tokenizer.current_token.value == '=='

def test_tokenize_delimiter():
    tokenizer = Tokenizer("(")
    tokenizer.selectNext()
    assert tokenizer.current_token.type == 'LIMITER'
    assert tokenizer.current_token.value == '('

def test_tokenize_eof():
    tokenizer = Tokenizer("EOF")
    tokenizer.selectNext()
    assert tokenizer.current_token.type == 'EOF'
    assert tokenizer.current_token.value is None

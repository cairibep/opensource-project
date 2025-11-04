import pytest
from PrePros import PrePros

def test_remove_simple_comment():
    prepros = PrePros("int x; /*comentario*/")
    result = prepros.removeComentarios()
    assert "/*comentario*/" not in result

def test_keep_code_without_comment():
    prepros = PrePros("int x;")
    result = prepros.removeComentarios()
    assert "int x;" in result

def test_remove_multiple_comments():
    prepros = PrePros("/*a*/ int x; /*b*/")
    result = prepros.removeComentarios()
    assert "a" not in result and "b" not in result


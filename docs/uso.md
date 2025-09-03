# Como Usar

## Compilar um código C de exemplo
```bash
python main.py testes.c
```

Isso irá gerar um arquivo `testes.asm` contendo a versão em Assembly.

## Fluxo do compilador

1. **Tokenização** → `Tokenizer.py` converte o código em tokens.
2. **Parsing** → `Parser.py` cria a AST (árvore sintática).
3. **Geração de Assembly** → `AsmWritter.py` escreve o código final.


---
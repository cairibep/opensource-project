# Tokenizer.py

Este módulo realiza a **análise léxica**.  
Ele transforma o código-fonte em uma lista de **tokens** que representam palavras-chave, identificadores, símbolos e literais.

## Funções principais
- Ler o código caractere por caractere.
- Reconhecer padrões de tokens.
- Tratar espaços em branco e comentários.
- Gerar uma sequência de tokens para o **Parser**.

## Exemplo de tokens
```text
int x = 10;
```

Tokens:

* `int`
* `x`
* `=`
* `10`
* `;`


---
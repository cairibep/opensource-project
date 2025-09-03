# AsmWritter.py

Responsável por **gerar o código Assembly** a partir da AST produzida pelo parser.  

## Funções principais
- Converter nós da AST em instruções assembly.
- Gerar um arquivo `.asm` como saída.
- Mapear variáveis e expressões para registradores/memória.

## Exemplo
Código C:
```c
int x = 5;
```

Saída Assembly (exemplo simplificado):

```asm
mov eax, 5
mov [x], eax
```

---
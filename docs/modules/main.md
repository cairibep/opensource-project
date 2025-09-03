# main.py

Este é o ponto de entrada do compilador.  
Ele coordena todas as etapas da compilação: leitura do código-fonte, tokenização, parsing e geração de código assembly.

## Funções principais
- Lê o arquivo `.c` de entrada.
- Chama o **Tokenizer** para análise léxica.
- Passa os tokens para o **Parser**.
- Executa o código em python, podendo ser configurado para criar um ASM.

## Exemplo
```bash
python main.py testes.c
```

---
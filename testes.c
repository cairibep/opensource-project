
int somar(int x, int y, int z) {
    int soma;
    soma = x + y + z; /* Soma */
    return soma;
}

int dobrar(int y) {
    y = y * 2; /* Dobra */
    return y;
}

int maior(int x, int y) {
    if (x > y) {
        return 1;
    }
    return 0;
}

void calcula_tudo() {
    /* Realiza calculos e imprime valor */
    int x;
    x = 5;

    int y;
    y = 100;

    while (maior(y, x) == 1) {
        printf(x);
        x = dobrar(x);
    }

    printf(y);
    printf(x);

    int res;
    res = somar(x, y, 1000);;

    printf(res);;;;
}

void main() {
    int x;
    int y;
    int z;
    x = 10;
    y = 20;
    z = 30;

    /* Realiza calculos */
    calcula_tudo();
    calcula_tudo();

    /* Variaveis nao devem ter sido alteradas na main */
    printf(x);
    printf(y);
    printf(z);
}
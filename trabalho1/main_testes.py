from testes.teste_stdout import teste_stdout
from testes.teste_arquivo import teste_leitura_arquivo, teste_escrita_arquivo
from testes.teste_tcp import teste_tcp_envia, teste_tcp_recebe
from testes.teste_stdin import teste_stdin

if __name__ == "__main__":
    teste_stdout()
    teste_leitura_arquivo()
    teste_tcp_envia()

    with open("saida_sebo.bin", "rb") as f:
        import sys
        sys.stdin = f
        teste_stdin()
    teste_escrita_arquivo()
    teste_tcp_recebe()
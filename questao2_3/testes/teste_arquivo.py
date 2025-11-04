from helpers.objetos import _objetos_demo
from livro_output_stream import LivroOutputStream

def teste_arquivo():
    print("\n=== Teste ii) Arquivo ===")
    with open("saida_sebo.bin", "wb") as f:
        stream = LivroOutputStream(_objetos_demo(), n_objetos=3, destino=f)
        stream.send_all()
    print("Gravado em 'saida_sebo.bin'.")
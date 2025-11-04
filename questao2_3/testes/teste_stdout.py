from helpers.objetos import _objetos_demo
from livro_output_stream import LivroOutputStream
import sys

def teste_stdout():
    print("\n=== Teste i) Saída padrão (bytes abaixo) ===")
    stream = LivroOutputStream(_objetos_demo(), n_objetos=3, destino=sys.stdout.buffer)
    stream.send_all()
    print("\n=== Fim do envio para stdout ===")
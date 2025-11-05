from testes.objetos import _objetos_demo
from streams.livro_output_stream import LivroOutputStream
from streams.livro_input_stream import LivroInputStream
import json

def teste_leitura_arquivo():
    print("\n=== Teste ii) Arquivo ===")
    with open("saida_sebo.bin", "wb") as f:
        stream = LivroOutputStream(_objetos_demo(), n_objetos=3, destino=f)
        stream.send_all()
    print("Gravado em 'saida_sebo.bin'.")

def teste_escrita_arquivo():
    print("\n=== Teste v) Escrita em arquivo ===")
    with open("saida_sebo.bin", "rb") as f:
        writer = LivroInputStream(f)
        objs = writer.read_all()
    print(f"[stdin] Lidos {len(objs)} objetos:")
    print(json.dumps(objs, ensure_ascii=False, indent=2))
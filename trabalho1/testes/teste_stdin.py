from streams.livro_input_stream import LivroInputStream
import sys
import json

def teste_stdin():
    print("\n=== Teste iv) Entrada padrão (stdin) ===")
    input_stream = sys.stdin.buffer if hasattr(sys.stdin, "buffer") else sys.stdin
    sis = LivroInputStream(input_stream)    
    objs = sis.read_all()
    print(json.dumps(objs, ensure_ascii=False, indent=2))
    print("=== Fim da leitura de stdin ===")
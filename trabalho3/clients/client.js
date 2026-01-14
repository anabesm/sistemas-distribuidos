const BASE = process.env.API_BASE || "http://127.0.0.1:8000";

async function request(endpoint, method = "GET", body = null) {
  const options = {
    method,
    headers: { "Content-Type": "application/json" },
  };

  if (body) options.body = JSON.stringify(body);

  const resp = await fetch(`${BASE}${endpoint}`, options);

  if (!resp.ok) {
    let err;
    try {
      err = await resp.json();
    } catch {
      const txt = await resp.text();
      throw new Error(`HTTP ${resp.status} -> ${txt}`);
    }
    throw new Error(err.detail || JSON.stringify(err));
  }

  if (resp.status === 204) return null;

  const txt = await resp.text();
  if (!txt) return null;
  try {
    return JSON.parse(txt);
  } catch {
    return txt;
  }
}

function produtoToString(p) {
  if (!p) return "Produto indefinido";

  const status = p.estado ? p.estado : (p.disponivel ? "disponível" : "vendido");
  const tipo = p.tipo_produto || "Produto";
  return `[${p.id}] ${p.titulo} – R$${Number(p.preco).toFixed(2)} – ${status} (${tipo})`;
}

async function main() {
  console.log("Conectando ao Servidor REST em:", BASE);

  try {
    console.log("\n== LISTANDO ==");
    const lista = await request("/produtos");

    if (!Array.isArray(lista)) {
      throw new Error("A API não retornou uma lista.");
    }
    lista.forEach((p) => console.log(produtoToString(p)));

    console.log("\n== BUSCA 'python' ==");
    const achados = await request("/produtos?termo=python");
    achados.forEach((p) => console.log(produtoToString(p)));

    console.log("\n== CADASTRANDO ==");

    const produtoTeste = {
      id: "T1",
      tipo_produto: "livro",
      titulo: "Livro de Teste (CRUD)",
      preco: 10.5,
      estado: "novo",
      extras: {
        autor: "Autor Teste",
        isbn: "TESTE-ISBN-0001",
        paginas: 123,
        genero: "Teste",
      },
    };

    try {
      await request(`/produtos/${produtoTeste.id}`);
      console.log(`Produto ${produtoTeste.id} já existia — deletando antes do cadastro...`);
      await request(`/produtos/${produtoTeste.id}`, "DELETE");
    } catch {
    }

    const cadastrado = await request("/produtos", "POST", produtoTeste);
    console.log("Cadastrado:", produtoToString(cadastrado));

    console.log("\n== CONFIRMANDO CADASTRO ==");
    const obtido = await request(`/produtos/${produtoTeste.id}`);
    console.log("Obtido:", produtoToString(obtido));


    console.log("\n== DELETANDO ==");
    await request(`/produtos/${produtoTeste.id}`, "DELETE");
    console.log(`OK: Produto ${produtoTeste.id} removido.`);



    console.log("\n== TROCA VÁLIDA: E1 <-> E2 ==");
    const resultadoTroca = await request("/transacoes/troca", "POST", {
      produto_a_id: "E1",
      produto_b_id: "E2",
    });
    console.log(resultadoTroca);

    console.log("\n== VENDA L2 ==");
    const respostaVenda = await request("/produtos/L2/venda", "POST");
    console.log(respostaVenda.mensagem);
    console.log("Item vendido:", produtoToString(respostaVenda.produto));

    console.log("\n== TROCA INVÁLIDA: E1 <-> L1 (ERRO ESPERADO) ==");
    try {
      await request("/transacoes/troca", "POST", {
        produto_a_id: "E1",
        produto_b_id: "L1",
      });
    } catch (e) {
      console.log("Erro capturado com sucesso:", e.message);
    }
  } catch (err) {
    console.error("Erro fatal na execução:", err.message);
    process.exit(1);
  }
}

main();
const BASE = process.env.API_BASE || "http://127.0.0.1:8000";

async function invoke(objectReference, methodId, args = [], kwargs = {}, requestId = 1) {
  const payload = {
    requestId,
    objectReference,
    methodId,
    arguments: { args, kwargs },
  };

  const resp = await fetch(`${BASE}/invoke`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!resp.ok) {
    let err;
    try {
      err = await resp.json();
    } catch {
      const txt = await resp.text();
      throw new Error(`HTTP ${resp.status} -> ${txt}`);
    }

    const detail = err.detail || err;
    throw new Error(detail.error || JSON.stringify(detail));
  }

  const data = await resp.json();

  if (data.isException) throw new Error(data.error || "Erro remoto");
  return data.result;
}

function produtoToString(p) {
  const status = p.disponivel ? "disponível" : "vendido";
  return `${p.__type__}(${p.id}) – ${p.titulo} – R$${Number(p.preco).toFixed(2)} – ${status}`;
}

async function main() {
  console.log("Servidor:", BASE);

  console.log("\n== LISTANDO ==");
  const lista = await invoke("CatalogoService", "listar");
  if (!Array.isArray(lista)) {
    console.log("Resposta inesperada em listar():", lista);
    throw new Error("listar() não retornou uma lista/array.");
  }
  lista.forEach(p => console.log(produtoToString(p)));

  console.log("\n== BUSCA 'python' ==");
  const achados = await invoke("CatalogoService", "buscar", ["python"]);
  achados.forEach(p => console.log(produtoToString(p)));

  console.log("\n== TROCA VÁLIDA: E1 <-> E2 ==");
  console.log(await invoke("TransacaoService", "trocar", ["E1", "E2"]));

  console.log("\n== VENDA L2 ==");
  const vendido = await invoke("TransacaoService", "vender", ["L2"]);
  console.log(produtoToString(vendido));

  console.log("\n== TROCA INVÁLIDA: E1 <-> L1 (ERRO ESPERADO) ==");
  try {
    console.log(await invoke("TransacaoService", "trocar", ["E1", "L1"]));
  } catch (e) {
    console.log("Erro esperado:", e.message);
  }
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});

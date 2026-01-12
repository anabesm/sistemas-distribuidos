const BASE = "http://127.0.0.1:8000";

async function invoke(objectReference, methodId, args = [], kwargs = {}, requestId = 1) {
  const payload = {
    requestId,
    objectReference,
    methodId,
    arguments: { args, kwargs }
  };

  const resp = await fetch(`${BASE}/invoke`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!resp.ok) {
    const err = await resp.json();
    const detail = err.detail || err;
    throw new Error(detail.error || JSON.stringify(detail));
  }

  const data = await resp.json();
  if (data.isException) throw new Error(data.error);
  return data.result;
}

function asListaProduto(result) {
  if (result && result.__kind__ === "ListaProduto") return result.value;
  return result;
}

function produtoToString(p) {
  const status = p.disponivel ? "disponível" : "vendido";
  return `${p.__type__}(${p.id}) – ${p.titulo} – R$${p.preco.toFixed(2)} – ${status}`;
}

async function main() {
  console.log("== LISTANDO ==");
  const lista = asListaProduto(await invoke("CatalogoService", "listar"));
  lista.forEach(p => console.log(produtoToString(p)));

  console.log("\n== BUSCA 'python' ==");
  const achados = asListaProduto(await invoke("CatalogoService", "buscar", ["python"]));
  achados.forEach(p => console.log(produtoToString(p)));

  console.log("\n== TROCA VÁLIDA: E1 <-> E2 ==");
  console.log(await invoke("TransacaoService", "trocar", ["E1", "E2"]));

  console.log("\n== VENDA L2 ==");
  const vendido = await invoke("TransacaoService", "vender", ["L2"]);
  if (vendido.__kind__ === "Produto") console.log(produtoToString(vendido.value));
  else console.log(vendido);

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

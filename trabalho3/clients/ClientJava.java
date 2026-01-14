import java.net.URI;
import java.net.http.*;
import java.nio.charset.StandardCharsets;

public class ClientJava {

    static final HttpClient client = HttpClient.newHttpClient();

    static HttpResponse<String> sendRequest(String url, String method, String jsonBody, boolean throwOnError) {
        try {
            HttpRequest.Builder builder = HttpRequest.newBuilder()
                    .uri(URI.create(url))
                    .header("Content-Type", "application/json");

            if ("POST".equalsIgnoreCase(method)) {
                String body = (jsonBody == null) ? "{}" : jsonBody;
                builder.POST(HttpRequest.BodyPublishers.ofString(body, StandardCharsets.UTF_8));
            } else if ("DELETE".equalsIgnoreCase(method)) {
                builder.DELETE();
            } else {
                builder.GET();
            }

            HttpRequest req = builder.build();
            HttpResponse<String> resp = client.send(req, HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));

            System.out.println("Status: " + resp.statusCode());
            if (resp.statusCode() == 204) {
                System.out.println("Response: (sem conteúdo)");
            } else {
                System.out.println("Response: " + resp.body());
            }

            if (throwOnError && (resp.statusCode() < 200 || resp.statusCode() >= 300)) {
                throw new RuntimeException("HTTP " + resp.statusCode() + " -> " + resp.body());
            }

            return resp;

        } catch (Exception e) {
            System.err.println("Erro na requisição: " + e.getMessage());
            if (throwOnError) {
                throw new RuntimeException(e);
            }
            return null;
        }
    }

    static HttpResponse<String> sendRequest(String url, String method, String jsonBody) {
        return sendRequest(url, method, jsonBody, false);
    }

    public static void main(String[] args) {
        String baseUrl = (args.length >= 1) ? args[0] : "http://127.0.0.1:8000";
        System.out.println("API URL: " + baseUrl);

        try {
            System.out.println("\n== LISTAR PRODUTOS ==");
            sendRequest(baseUrl + "/produtos", "GET", null, true);

            System.out.println("\n== BUSCAR 'python' ==");
            sendRequest(baseUrl + "/produtos?termo=python", "GET", null, true);

            String produtoId = "T1";

            System.out.println("\n== CADASTRANDO ==");
            String jsonCadastrar = "{"
                    + "\"id\":\"" + produtoId + "\","
                    + "\"tipo_produto\":\"livro\","
                    + "\"titulo\":\"Livro de Teste (CRUD)\","
                    + "\"preco\":10.5,"
                    + "\"estado\":\"novo\","
                    + "\"extras\":{"
                    +   "\"autor\":\"Autor Teste\","
                    +   "\"isbn\":\"TESTE-ISBN-0001\","
                    +   "\"paginas\":123,"
                    +   "\"genero\":\"Teste\""
                    + "}"
                    + "}";


            sendRequest(baseUrl + "/produtos", "POST", jsonCadastrar, true);


            System.out.println("\n== DELETANDO ==");
            sendRequest(baseUrl + "/produtos/" + produtoId, "DELETE", null, true);
            System.out.println("OK: Produto " + produtoId + " deletado.");

            System.out.println("\n== TROCA VÁLIDA E1 <-> E2 ==");
            String jsonTrocaValida = "{"
                    + "\"produto_a_id\": \"E1\","
                    + "\"produto_b_id\": \"E2\""
                    + "}";
            sendRequest(baseUrl + "/transacoes/troca", "POST", jsonTrocaValida, true);

            System.out.println("\n== VENDA L2 ==");
            sendRequest(baseUrl + "/produtos/L2/venda", "POST", "{}", true);

            System.out.println("\n== TROCA INVÁLIDA E1 <-> L1 (ERRO ESPERADO) ==");
            String jsonTrocaInvalida = "{"
                    + "\"produto_a_id\": \"E1\","
                    + "\"produto_b_id\": \"L1\""
                    + "}";
            try {
                sendRequest(baseUrl + "/transacoes/troca", "POST", jsonTrocaInvalida, true);
                System.out.println("ERRO: troca inválida não falhou como esperado!");
            } catch (Exception e) {
                System.out.println("Erro capturado com sucesso: " + e.getMessage());
            }

        } catch (Exception fatal) {
            System.err.println("Erro fatal na execução: " + fatal.getMessage());
            System.exit(1);
        }
    }
}

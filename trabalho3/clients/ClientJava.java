import java.net.URI;
import java.net.http.*;
import java.nio.charset.StandardCharsets;

public class ClientJava {

    static final HttpClient client = HttpClient.newHttpClient();

    static void sendRequest(String url, String method, String jsonBody) {
        try {
            HttpRequest.Builder builder = HttpRequest.newBuilder()
                    .uri(URI.create(url))
                    .header("Content-Type", "application/json");

            if ("POST".equalsIgnoreCase(method)) {
                builder.POST(HttpRequest.BodyPublishers.ofString(jsonBody, StandardCharsets.UTF_8));
            } else {
                builder.GET();
            }

            HttpRequest req = builder.build();
            HttpResponse<String> resp = client.send(req, HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));

            System.out.println("Status: " + resp.statusCode());

            System.out.println("Response: " + resp.body());

        } catch (Exception e) {
            System.err.println("Erro na requisição: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        String baseUrl = (args.length >= 1) ? args[0] : "http://127.0.0.1:8000";
        System.out.println("API URL: " + baseUrl);

        System.out.println("\n== LISTAR PRODUTOS ==");
        sendRequest(baseUrl + "/produtos", "GET", null);

        System.out.println("\n== BUSCAR 'python' ==");
        sendRequest(baseUrl + "/produtos?termo=python", "GET", null);

        System.out.println("\n== TROCA VÁLIDA E1 <-> E2 ==");
        String jsonTrocaValida = "{"
                + "\"produto_a_id\": \"E1\","
                + "\"produto_b_id\": \"E2\""
                + "}";
        sendRequest(baseUrl + "/transacoes/troca", "POST", jsonTrocaValida);

        System.out.println("\n== TROCA INVÁLIDA E1 <-> L1 (ERRO ESPERADO) ==");
        String jsonTrocaInvalida = "{"
                + "\"produto_a_id\": \"E1\","
                + "\"produto_b_id\": \"L1\""
                + "}";
        sendRequest(baseUrl + "/transacoes/troca", "POST", jsonTrocaInvalida);
        
        System.out.println("\n== VENDA L2 ==");
        sendRequest(baseUrl + "/produtos/L2/venda", "POST", "{}");
    }
}
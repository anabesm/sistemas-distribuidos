import java.net.URI;
import java.net.http.*;
import java.nio.charset.StandardCharsets;

public class ClientJava {
    static final String BASE = "http://127.0.0.1:8000/invoke";
    static final HttpClient client = HttpClient.newHttpClient();

    static String invokeJson(String objectRef, String methodId, String argsJson) throws Exception {
        // argsJson: ex "[]" ou "[\"E1\",\"E2\"]"
        String body = "{"
                + "\"requestId\":1,"
                + "\"objectReference\":\"" + objectRef + "\","
                + "\"methodId\":\"" + methodId + "\","
                + "\"arguments\":{\"args\":" + argsJson + ",\"kwargs\":{}}"
                + "}";

        HttpRequest req = HttpRequest.newBuilder()
                .uri(URI.create(BASE))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(body, StandardCharsets.UTF_8))
                .build();

        HttpResponse<String> resp = client.send(req, HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));

        if (resp.statusCode() >= 400) {
            throw new RuntimeException("HTTP " + resp.statusCode() + " -> " + resp.body());
        }
        return resp.body();
    }

    public static void main(String[] args) throws Exception {
        System.out.println("== LISTAR ==");
        System.out.println(invokeJson("CatalogoService", "listar", "[]"));

        System.out.println("\n== TROCA VÁLIDA E1 <-> E2 ==");
        System.out.println(invokeJson("TransacaoService", "trocar", "[\"E1\",\"E2\"]"));

        System.out.println("\n== TROCA INVÁLIDA E1 <-> L1 (ERRO ESPERADO) ==");
        try {
            System.out.println(invokeJson("TransacaoService", "trocar", "[\"E1\",\"L1\"]"));
        } catch (Exception e) {
            System.out.println("Erro esperado: " + e.getMessage());
        }
    }
}

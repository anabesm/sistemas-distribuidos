import java.net.URI;
import java.net.http.*;
import java.nio.charset.StandardCharsets;

public class ClientJava {

    static final HttpClient client = HttpClient.newHttpClient();

    static String invokeJson(String invokeUrl, String objectRef, String methodId, String argsJson) throws Exception {
        String body = "{"
                + "\"requestId\":1,"
                + "\"objectReference\":\"" + objectRef + "\","
                + "\"methodId\":\"" + methodId + "\","
                + "\"arguments\":{\"args\":" + argsJson + ",\"kwargs\":{}}"
                + "}";

        HttpRequest req = HttpRequest.newBuilder()
                .uri(URI.create(invokeUrl))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(body, StandardCharsets.UTF_8))
                .build();

        HttpResponse<String> resp = client.send(req, HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
        return resp.body();
    }

    public static void main(String[] args) throws Exception {
        String invokeUrl = (args.length >= 1) ? args[0] : "http://127.0.0.1:8000/invoke";
        System.out.println("Invoke URL: " + invokeUrl);

        System.out.println("\n== LISTAR ==");
        System.out.println(invokeJson(invokeUrl, "CatalogoService", "listar", "[]"));

        System.out.println("\n== TROCA VALIDA E1 <-> E2 ==");
        System.out.println(invokeJson(invokeUrl, "TransacaoService", "trocar", "[\"E1\",\"E2\"]"));

        System.out.println("\n== TROCA INVALIDA E1 <-> L1 (ERRO ESPERADO) ==");
        System.out.println(invokeJson(invokeUrl, "TransacaoService", "trocar", "[\"E1\",\"L1\"]"));
    }
}

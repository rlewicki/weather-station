package tech.rlewicki.WeatherStation;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import org.apache.commons.codec.binary.Hex;
import org.springframework.web.bind.annotation.*;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("api/v1/sampleReading")
public class SampleReadingController {
    private final SampleReadingService service;
    private final String secretKey;
    private final String secretKeyEnvVariableName = "WEATHER_STATION_SECRET_KEY";
    private final String headerEntry = "x-signature-sha256";

    public SampleReadingController(SampleReadingService service) {
        this.service = service;

        secretKey = System.getenv(secretKeyEnvVariableName);
        if (secretKey.isEmpty()) {
            System.out.println("Missing secret key definition in environment variables!");
        }
    }

    // Fetching data should also be protected by comparing SHA256 signature.
    @GetMapping("all")
    public List<SampleReading> fetchAllSampleReadings() {
        return service.getAllSampleReadings();
    }

    @CrossOrigin
    @GetMapping("last_count")
    public List<SampleReading> fetchSampleReadings(@RequestParam int count) {
        return service.getSampleReadings(count);
    }

    @PostMapping("insert_single")
    public int insertSingleSampleReading(@RequestHeader Map<String, String> header, @RequestBody Map<String, String> body) {
        if (!header.containsKey(headerEntry)) {
            System.out.println("Request header is missing " + headerEntry);
            return 400;
        }

        String headerChecksum = header.get(headerEntry);
        if (!verifySignature(headerChecksum, body, secretKey)) {
            System.out.println(headerEntry + " mismatch");
            return 400;
        }

        final ObjectMapper objectMapper = new ObjectMapper();
        objectMapper.registerModule(new JavaTimeModule());
        SampleReading sampleReading = objectMapper.convertValue(body, SampleReading.class);
        service.insertSampleReading(sampleReading);
        return 200;
    }

    private static boolean verifySignature(String requestChecksum, Map<String, String> body, String privateKey) {
        final String encodingAlgorithm = "HmacSHA256";
        try {
            Mac hmac = Mac.getInstance(encodingAlgorithm);
            SecretKeySpec keySpec = new SecretKeySpec(privateKey.getBytes(), encodingAlgorithm);
            hmac.init(keySpec);
            hmac.update("temperature".getBytes());
            hmac.update(body.get("temperature").getBytes());
            hmac.update("humidity".getBytes());
            hmac.update(body.get("humidity").getBytes());
            byte[] checksumBytes = hmac.doFinal();
            String checksumString = Hex.encodeHexString(checksumBytes);
            return requestChecksum.equals(checksumString);
        } catch (NoSuchAlgorithmException | InvalidKeyException e) {
            e.printStackTrace();
        }

        return false;
    }
}

package tech.rlewicki.WeatherStation;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.time.LocalDateTime;
import java.time.ZoneId;

@Data
@Document
public class SampleReading {
    @Id
    String id;
    LocalDateTime date;
    float temperature;
    float humidity;

    public SampleReading(LocalDateTime date, float temperature, float humidity) {
        this.date = date;
        this.temperature = temperature;
        this.humidity = humidity;
    }

    public SampleReading() {
        LocalDateTime gmtTime = LocalDateTime.now(ZoneId.of("GMT"));
        this.date = gmtTime.plusHours(2);
    }
}

package tech.rlewicki.WeatherStation;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import java.time.LocalDateTime;

@SpringBootApplication
public class WeatherStationApplication {

	public static void main(String[] args) {
		SpringApplication.run(WeatherStationApplication.class, args);
	}

//	@Bean
//	CommandLineRunner runner(SampleReadingRepository repository) {
//		return args -> {
//			SampleReading sampleReading = new SampleReading(LocalDateTime.now(), 25.0f, 50.0f);
//			repository.insert(sampleReading);
//		};
//	}
}

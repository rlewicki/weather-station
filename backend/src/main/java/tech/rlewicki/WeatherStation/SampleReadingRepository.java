package tech.rlewicki.WeatherStation;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface SampleReadingRepository extends MongoRepository<SampleReading, String> {
}

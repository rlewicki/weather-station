package tech.rlewicki.WeatherStation;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@AllArgsConstructor
@Service
public class SampleReadingService {
    private final SampleReadingRepository repository;

    public List<SampleReading> getAllSampleReadings() {
        return repository.findAll();
    }
    public void insertSampleReading(SampleReading sampleReading) {
        repository.insert(sampleReading);
    }
}

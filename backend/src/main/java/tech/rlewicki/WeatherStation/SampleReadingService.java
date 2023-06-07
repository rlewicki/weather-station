package tech.rlewicki.WeatherStation;

import lombok.AllArgsConstructor;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Service;

import java.util.List;

@AllArgsConstructor
@Service
public class SampleReadingService {
    private final SampleReadingRepository repository;
    private final MongoTemplate mongoTemplate;

    public List<SampleReading> getAllSampleReadings() {
        return repository.findAll();
    }
    public void insertSampleReading(SampleReading sampleReading) {
        repository.insert(sampleReading);
    }

    public List<SampleReading> getSampleReadings(int count) {
        long lastIndex = repository.count() - 1;
        long firstIndex = lastIndex - count;
        if (firstIndex < 0) {
            firstIndex = 0;
        }

        return repository.findAll().subList((int)firstIndex, (int)lastIndex);
    }

    public SampleReading getLastSample() {
        Query query = new Query();
        query.limit(1);
        query.with(Sort.by(Sort.Order.desc("date")));
        List<SampleReading> samples = mongoTemplate.find(query, SampleReading.class);
        if (samples.size() > 0) {
            return samples.get(0);
        }
        else {
            return null;
        }
    }
}

package org.example.web1.repo;

import java.util.List;
import java.util.Optional;

public interface SingerRepo {
    public Optional<String> findNameById(int id);
}
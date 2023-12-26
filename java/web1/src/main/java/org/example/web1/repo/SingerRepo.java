package org.example.web1.repo;

import java.util.List;
import java.util.Optional;
import java.util.Set;

public interface SingerRepo {
    public Optional<String> findNameById(int id);
    public Set<String> findByName(String filter);
}
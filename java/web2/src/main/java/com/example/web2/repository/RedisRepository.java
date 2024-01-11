package com.example.web2.repository;

import com.example.web2.model.UserRedisEntry;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface RedisRepository extends CrudRepository<UserRedisEntry, String> {
}

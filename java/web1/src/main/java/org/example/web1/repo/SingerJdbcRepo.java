package org.example.web1.repo;

import java.util.Optional;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.jdbc.support.KeyHolder;
import org.springframework.stereotype.Repository;



@Repository("singerRepo")
public class SingerJdbcRepo implements SingerRepo {
    private static final Logger LOGGER = LoggerFactory.getLogger(SingerJdbcRepo.class);
    private JdbcTemplate jdbcTemplate;

    @Autowired
    public void setJdbcTemplate(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    public Optional<String> findNameById(int id) {

        var name = jdbcTemplate.queryForObject("select count(*) from SINGER", String.class);
        if (name == null) return Optional.empty();

        return Optional.of(name);

    }


}
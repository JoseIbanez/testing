package org.example.web1.repo;

import java.sql.ResultSet;
import java.sql.SQLDataException;
import java.sql.SQLException;
import java.util.HashSet;
import java.util.Optional;
import java.util.Set;

import org.example.web1.model.SingerRecord;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.jdbc.support.KeyHolder;
import org.springframework.stereotype.Repository;



@Repository("singerRepo")
public class SingerJdbcRepo implements SingerRepo {
    private static final Logger logger = LoggerFactory.getLogger(SingerJdbcRepo.class);
    private JdbcTemplate jdbcTemplate;

    @Autowired
    public void setJdbcTemplate(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    public Optional<String> findNameById(int id) {

        var name = jdbcTemplate.queryForObject("select id,first_name,last_name from SINGER where id = ?", new SingerStringMapper(), id);
        if (name == null) return Optional.empty();

        return Optional.of(name);

    }

    public Set<String> findByName(String filter) {

        var stream = jdbcTemplate.queryForStream("select id,first_name,last_name from SINGER where first_name like ?",new SingerStringMapper(), filter);

        Set<String> result = new HashSet<String>();

        result.add("Test");

        var iterator = stream.iterator();

        while (iterator.hasNext()) {
            result.add(iterator.next());
        }

        logger.info("Found: {}",result.toString());
        return result;

    }




    static class SingerStringMapper implements RowMapper<String> {

        @Override
        public String mapRow(ResultSet rs, int rowNum) throws SQLDataException, SQLException {

            String result = String.format("Singer(%d): %s %s",
                    rs.getLong("id"),
                    rs.getString("first_name"),
                    rs.getString("last_name"));

            logger.info("Found Singer: {}", rs.getLong("id"));

            return result;
        }
    }

    static class SingerMapper implements RowMapper<SingerRecord.Singer> {

        @Override
        public SingerRecord.Singer mapRow(ResultSet rs, int rowNum) throws SQLDataException, SQLException {

            SingerRecord.Singer result = new SingerRecord.Singer(
                    rs.getLong("id"),
                    rs.getString("first_name"),
                    rs.getString("last_name")
            );

            logger.info("Found Singer: {}",rs.getLong("id"));

            return result;
        }



    }

}
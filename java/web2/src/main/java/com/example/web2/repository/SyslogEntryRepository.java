package com.example.web2.repository;

import com.example.web2.model.SyslogEntry;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface SyslogEntryRepository extends JpaRepository<SyslogEntry, Long> {
}

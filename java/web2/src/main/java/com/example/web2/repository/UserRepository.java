package com.example.web2.repository;


import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import com.example.web2.model.User;

@Repository
public interface UserRepository extends JpaRepository<User, Long>,CustomUserRepository {

}
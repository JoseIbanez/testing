package com.example.web2.repository;

import com.example.web2.model.User;

import java.util.stream.Stream;

public interface CustomUserRepository {

    User customFind(Long id);
    Stream<User> customFindByName(String filter);

}

package com.example.web2.repository;

import com.example.web2.model.User;
import jakarta.annotation.PostConstruct;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;

import java.util.Objects;
import java.util.stream.Stream;

public class CustomUserRepositoryImpl implements CustomUserRepository {

    @PersistenceContext
    private EntityManager entityManager;

    @Override
    public User customFind(Long id) {
        User user = (User) entityManager.createQuery("FROM User u WHERE u.id = :id")
                .setParameter("id",id)
                .getSingleResult();
        return user;
    }

    @Override
    public  Stream<User> customFindByName(String filter) {
        var stream = entityManager.createQuery("FROM User u WHERE u.name like :filter")
                .setParameter("filter",filter)
                .getResultList()
                .stream();

        return stream;
    }



    @PostConstruct
    public void postConstruct() {
        Objects.requireNonNull(entityManager);
    }

}

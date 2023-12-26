package com.example.web2;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.example.web2.model.User;
import com.example.web2.repository.UserRepository;

import java.util.Optional;


@SpringBootTest(classes = Web2Application.class)
class CustomRepositoryUnitTest {

    @Autowired
    private UserRepository userRepository;

    @Test
    void givenCustomRepository_whenInvokeCustomFindMethod_thenEntityIsFound() {
        User user = new User();
        user.setEmail("foo@gmail.com");
        user.setName("userName");

        User persistedUser = userRepository.save(user);
        Long userId = persistedUser.getId();

        Optional<User> user1 = userRepository.findById(userId);

        assertEquals(persistedUser,user1.get());


        assertEquals(persistedUser, userRepository.customFind(user.getId()));
    }
}

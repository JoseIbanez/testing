package com.example.web2;

import org.junit.jupiter.api.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.example.web2.model.User;
import com.example.web2.repository.UserRepository;

import java.util.Optional;
import java.util.stream.Stream;


@SpringBootTest(classes = Web2Application.class)
class CustomRepositoryUnitTest {

    private static final Logger logger = LoggerFactory.getLogger(CustomRepositoryUnitTest.class);


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

    @Test
    void customFindByName() {

        Stream<User> userStream2 = userRepository.customFindByName("%u%");

        userStream2.forEach( u -> {
            logger.info("Found {} {}", u.getId(), u.getName());
        });



    }


}

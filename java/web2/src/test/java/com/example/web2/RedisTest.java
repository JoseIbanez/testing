package com.example.web2;

import com.example.web2.model.UserRedisEntry;
import com.example.web2.repository.RedisRepository;
import com.example.web2.repository.SyslogEntryRepository;
import com.example.web2.repository.UserRepository;
import com.example.web2.service.ImportElasticService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.integration.redis.util.RedisLockRegistry;
import org.springframework.integration.support.locks.ExpirableLockRegistry;
import org.springframework.test.context.junit.jupiter.SpringExtension;

import java.util.Optional;
import java.util.concurrent.locks.Lock;


@ExtendWith(SpringExtension.class)
@SpringBootTest(classes = Web2Application.class)
public class RedisTest {
    private static final Logger logger = LoggerFactory.getLogger(RedisTest.class);


    @Autowired
    private RedisRepository redisRepository;

    @Autowired
    RedisConnectionFactory redisConnectionFactory;

    @Qualifier("LOCK_REGISTRY_BEAN")
    @Autowired
    private ExpirableLockRegistry lockRegistry;
    @Test
    public void userRepositoryTest() throws Exception {

        UserRedisEntry user = new UserRedisEntry("U001", "Antonio Sanchez");

        redisRepository.save(user);

        UserRedisEntry redisUser = redisRepository.findById("U001").get();
        logger.info("Redis User:{}",redisUser);

        redisRepository.findById("U002").ifPresent(userRedisEntry ->
                logger.info("Redis User:{}", userRedisEntry));





    }

    @Test
    public void redisLockTest() throws Exception {

        Lock lock1 = lockRegistry.obtain("key1");
        Lock lock2 = lockRegistry.obtain("key1");

        logger.info("lock1: {}", lock1.tryLock() ? "Fetched" : "Locked");

        for (int i=1; i<30; i++ ){
            logger.info("lock2: {}", lock2.tryLock() ? "Fetched" : "Locked");
            Thread.sleep(1*1000);
        }

        logger.info("END");


    }


    @Test
    public void redisLockTest02() throws Exception {

        RedisLockRegistry redisLockRegistry1 = new RedisLockRegistry(redisConnectionFactory, "Key1", 10 * 1000);
        Lock lock1 = redisLockRegistry1.obtain("key1.1");

        Lock lock2 = new RedisLockRegistry(redisConnectionFactory, "Key1", 10 * 1000).
                obtain("key1.1");
        Lock lock3 = new RedisLockRegistry(redisConnectionFactory, "Key1", 10 * 1000).
                obtain("key1.1");



        for (int i=1; i<20; i++ ){

            logger.info("lock1: {}", lock1.tryLock() ? "Fetched" : "Locked");
            logger.info("lock2: {}", lock2.tryLock() ? "Fetched" : "Locked");
            logger.info("lock3: {}", lock3.tryLock() ? "Fetched" : "Locked");
            Thread.sleep(1 * 1000);
        }

        logger.info("END");

    }
}
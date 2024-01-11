package com.example.web2;

import com.example.web2.model.UserRedisEntry;
import com.example.web2.repository.RedisRepository;
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

import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.ssm.SsmClient;
import software.amazon.awssdk.services.ssm.model.GetParameterRequest;
import software.amazon.awssdk.services.ssm.model.GetParameterResponse;
import software.amazon.awssdk.services.ssm.model.SsmException;

import java.util.concurrent.locks.Lock;


@ExtendWith(SpringExtension.class)
@SpringBootTest(classes = Web2Application.class)
public class AwsSsmTest {
    private static final Logger logger = LoggerFactory.getLogger(AwsSsmTest.class);




    @Test
    public void ssmTest() throws Exception,SsmException {


        //var paraName = "/develop-eks/kafka";
        var paraName = "/develop/topicList";

        SsmClient ssmClient = SsmClient.builder().build();

        GetParameterRequest parameterRequest = GetParameterRequest.builder()
                .name(paraName)
                .withDecryption(Boolean.TRUE)
                .build();

        GetParameterResponse parameterResponse = ssmClient.getParameter(parameterRequest);
        String parameterValue = parameterResponse.parameter().value();
        ssmClient.close();

        System.out.println("The parameter value is " + parameterValue);


    }


}
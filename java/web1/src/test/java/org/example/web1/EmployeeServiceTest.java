package org.example.web1;

import static org.springframework.test.web.client.match.MockRestRequestMatchers.method;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.requestTo;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withStatus;

import java.net.URI;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.web.client.ExpectedCount;
import org.springframework.test.web.client.MockRestServiceServer;
import org.springframework.test.web.client.RequestMatcher;
import org.springframework.test.web.client.ResponseActions;
import org.springframework.web.client.RestTemplate;

import org.example.web1.SpringTestConfig;
import org.example.web1.model.Employee;
import org.example.web1.service.EmployeeService;
import com.fasterxml.jackson.databind.ObjectMapper;

@ExtendWith(SpringExtension.class)
@SpringBootTest(classes = SpringTestConfig.class)
public class EmployeeServiceTest {

    private static final Logger logger = LoggerFactory.getLogger(EmployeeServiceTest.class);

    @Autowired
    private EmployeeService empService;

    @Autowired
    private RestTemplate restTemplate;

    private MockRestServiceServer mockServer;

    private ObjectMapper mapper = new ObjectMapper();

    @BeforeEach
    public void init() {
        mockServer = MockRestServiceServer.createServer(restTemplate);
    }

    public void simpleExpect(String uri, Object answer) throws Exception {

        mockServer.expect(ExpectedCount.once(), requestTo(new URI(uri)))
                .andExpect(method(HttpMethod.GET))
                .andRespond(withStatus(HttpStatus.OK)
                        .contentType(MediaType.APPLICATION_JSON)
                        .body(mapper.writeValueAsString(answer)));

    }

    @Test
    public void test01() throws Exception {
        Employee emp1 = new Employee("E001", "Eric Simmons");
        Employee emp2 = new Employee("E002", "Eric Simmons");

        simpleExpect("http://localhost:8080/employee/E001", emp1);
        simpleExpect("http://localhost:8080/employee/E002", emp2);


        Employee employee1 = empService.getEmployee("E001");
        logger.info("Employee, Id:{} Name:{}",employee1.getId(), employee1.getName());
        Assertions.assertEquals(emp1, employee1);

        Employee employee2 = empService.getEmployee("E002");
        logger.info("Employee, Id:{} Name:{}",employee2.getId(), employee2.getName());
        Assertions.assertEquals(emp2, employee2);

        mockServer.verify();
    }

}
package org.example.web1;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.example.web1.idmPojo.IdmEmployeePojo;
import org.example.web1.model.Employee;
import org.example.web1.service.EmployeeService;
import org.example.web1.service.IdmEmployeeService;
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
import org.springframework.web.client.RestTemplate;

import java.net.URI;
import java.nio.charset.StandardCharsets;

import static org.springframework.test.web.client.match.MockRestRequestMatchers.method;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.requestTo;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withStatus;



@ExtendWith(SpringExtension.class)
@SpringBootTest(classes = SpringTestConfig.class)
public class IdmEmployeeServiceTest {

    private static final Logger logger = LoggerFactory.getLogger(EmployeeServiceTest.class);

    @Autowired
    private IdmEmployeeService idmEmployeeService;

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

    public void simpleExpect(String uri, String body) throws Exception {

        mockServer.expect(ExpectedCount.once(), requestTo(new URI(uri)))
                .andExpect(method(HttpMethod.GET))
                .andRespond(withStatus(HttpStatus.OK)
                        .contentType(MediaType.APPLICATION_JSON)
                        .body(body));

    }

    public void simpleExpectFromFile(String uri, String filename) throws Exception {

        var bodyStream = this.getClass().getResourceAsStream("/"+filename).readAllBytes();
        var body = new String(bodyStream, StandardCharsets.UTF_8);

        logger.info("URI:{}, Filename:{} Body:{}",uri,filename,
                body.replace("\n","").replace("  "," "));

        simpleExpect(uri,body);
    }







    @Test
    public void test01() throws Exception {

        simpleExpectFromFile("http://localhost:8080/employees", "employeeList-01.json");

        String result = idmEmployeeService.downloadEmployees();
        logger.info("Message: {}",result);

        IdmEmployeePojo emp1 = idmEmployeeService.getIdmEmployee(1);
        logger.info(emp1.toString());

        for (var emp: idmEmployeeService.getIdmEmployees()) {
            logger.info("{} -> {}",emp.toString(), emp.toEmployee().toString());
        }

        mockServer.verify();
    }



}
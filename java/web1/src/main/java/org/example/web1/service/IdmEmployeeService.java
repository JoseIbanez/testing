package org.example.web1.service;

import org.example.web1.idmPojo.IdmEmployeeListResponsePojo;
import org.example.web1.idmPojo.IdmEmployeePojo;
import org.example.web1.model.Employee;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.List;

@Service
public class IdmEmployeeService {

    private static final Logger logger = LoggerFactory.getLogger(EmployeeService.class);

    private IdmEmployeeListResponsePojo idmResponse;

    @Autowired
    private RestTemplate restTemplate;

    public String downloadEmployees() {

        ResponseEntity<IdmEmployeeListResponsePojo> resp = restTemplate.getForEntity("http://localhost:8080/employees",
                IdmEmployeeListResponsePojo.class);

        if (resp.getStatusCode() != HttpStatus.OK) {
            return resp.getStatusCode().toString();
        }
        idmResponse = resp.getBody();

        return idmResponse.getMessage();

    }

    public List<IdmEmployeePojo> getIdmEmployees() {
        return this.idmResponse.getData();
    }

    public IdmEmployeePojo getIdmEmployee(int index) {
        return idmResponse.getData().get(index);
    }



    public int size() {
        return idmResponse.getData().size();
    }

}
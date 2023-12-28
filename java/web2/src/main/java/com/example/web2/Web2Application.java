package com.example.web2;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import com.example.web2.service.ImportElasticService;


@SpringBootApplication
public class Web2Application {

	private static final Logger logger = LoggerFactory.getLogger(Web2Application.class);


	public static void main(String[] args) {
		SpringApplication.run(Web2Application.class, args);

		logger.info("hi there!");



	}

}

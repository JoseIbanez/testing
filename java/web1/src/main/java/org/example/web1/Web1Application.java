package org.example.web1;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;


@SpringBootApplication
public class Web1Application {

	private static final Logger logger = LoggerFactory.getLogger((Web1Application.class));

	public static void main(String[] args) {

		SpringApplication.run(Web1Application.class, args);
		logger.info("Hi {} {}","java","!");

	}

}

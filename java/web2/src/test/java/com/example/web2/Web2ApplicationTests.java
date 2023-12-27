package com.example.web2;

import com.example.web2.config.SpringTestConfig;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
@SpringBootTest(classes = SpringTestConfig.class)
public class Web2ApplicationTests {

	@Test
	void contextLoads() {
	}

}

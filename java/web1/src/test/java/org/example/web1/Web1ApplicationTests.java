package org.example.web1;

import org.example.web1.config.SpringTestConfig;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
@SpringBootTest(classes = SpringTestConfig.class)
class Web1ApplicationTests {

	@Test
	void contextLoads() {
	}

}

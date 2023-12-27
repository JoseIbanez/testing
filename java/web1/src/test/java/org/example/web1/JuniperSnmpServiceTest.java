package org.example.web1;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.example.web1.config.SpringTestConfig;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
@SpringBootTest(classes = SpringTestConfig.class)
public class JuniperSnmpServiceTest {
    private static final Logger logger = LoggerFactory.getLogger(JuniperSnmpServiceTest.class);

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    public void unstructuredJson() throws Exception {

        String filename = "device_config_template_3.json";

        var fileStream = this.getClass().getResourceAsStream("/"+filename);
        JsonNode input = objectMapper.readTree(fileStream);


        for ( var device: input ) {

            String device_name = device.get("name").asText();
            logger.info("device:{}", device_name);

            var template_list = device.at("/output/template_config");
            for (var template: template_list ) {

                JsonNode fq_name_list = template.at("/abstract_config/fq_name");
                if (fq_name_list.isMissingNode()) { continue; }
                String fq_name = fq_name_list.get(fq_name_list.size() - 1).asText();
                logger.info(" device:{} abstract_config:{}",device_name,fq_name);

                var snmpUsers = template.at("/abstract_config/candidate_config/config_blob/configuration/snmp/snmpv3_users");
                if (snmpUsers.isMissingNode())  continue;
                //logger.info(" device:{} snmpUsers:{}",device_name,snmpUsers);

                for (var snmpUser: snmpUsers ) {
                    var user = snmpUser.path("snmp_user");
                    if (user.isMissingNode()) continue;;
                    logger.info("  Device:{} template:{} snmpv3User:{}",device_name, fq_name, user.asText());

                }


            }


        }


    }




}

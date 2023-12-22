package org.example.web1.api;

import org.example.web1.model.Car;
import org.example.web1.repo.SingerRepo;
import org.example.web1.service.CarService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.lang.invoke.MethodHandles;
import java.util.List;


@RequestMapping("api/v1/singer")
@RestController
public class SingerController {

    private static final Logger logger = LoggerFactory.getLogger((MethodHandles.lookup().lookupClass()));

    @Autowired
    SingerRepo singerRepo;

    @GetMapping
    public String selectAllSingers() {

        var name = singerRepo.findNameById(1);
        logger.info("name:{}",name.toString());

        return name.toString();
    }

}
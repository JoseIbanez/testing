package org.example.web1.api;

import java.io.Serializable;
import java.util.Date;

import org.springframework.core.serializer.Serializer;
import org.springframework.http.HttpStatus;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.reactive.result.method.annotation.ResponseEntityExceptionHandler;
import org.springframework.web.server.ResponseStatusException;


@ControllerAdvice
public class RestExceptionHandler extends ResponseEntityExceptionHandler {

    //@ExceptionHandler(value = ResponseStatusException.class)
    protected ResponseEntity<Object> handleConflict(ResponseStatusException ex) {
        ErrorResponse errorResponse = new ErrorResponse(ex.getStatusCode(),ex.getReason());
        return new ResponseEntity<>(errorResponse, ex.getStatusCode());
    }

    @ExceptionHandler(value = RuntimeException.class)
    protected ResponseEntity<Object> handleConflict(RuntimeException ex) {
        HttpStatus statusCode = HttpStatus.INTERNAL_SERVER_ERROR;
        ErrorResponse errorResponse = new ErrorResponse(statusCode,ex.getMessage());
        return new ResponseEntity<>(errorResponse, statusCode);
    }


}



class ErrorResponse {
    // customizing timestamp serialization format
    //@JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "dd-MM-yyyy hh:mm:ss")
    private Date timestamp;


    private int code;

    private String status;

    private String message;

    private String stackTrace;

    private Object data;

    public ErrorResponse() {
        timestamp = new Date();
    }

    public ErrorResponse(
            HttpStatusCode httpStatus,
            String message
    ) {
        this();
        this.code = httpStatus.value();
        this.status = httpStatus.toString();
        this.message = message;
    }

    public ErrorResponse(
            HttpStatus httpStatus,
            String message
    ) {
        this();
        this.code = httpStatus.value();
        this.status = httpStatus.toString();
        this.message = message;
    }

    public ErrorResponse(
            HttpStatus httpStatus,
            String message,
            String stackTrace
    ) {
        this(
                httpStatus,
                message
        );

        this.stackTrace = stackTrace;
    }

    public ErrorResponse(
            HttpStatus httpStatus,
            String message,
            String stackTrace,
            Object data
    ) {
        this(
                httpStatus,
                message,
                stackTrace
        );

        this.data = data;
    }



    public Date getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Date timestamp) {
        this.timestamp = timestamp;
    }

    public int getCode() {
        return code;
    }

    public void setCode(int code) {
        this.code = code;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getStackTrace() {
        return stackTrace;
    }

    public void setStackTrace(String stackTrace) {
        this.stackTrace = stackTrace;
    }

    public Object getData() {
        return data;
    }

    public void setData(Object data) {
        this.data = data;
    }




}
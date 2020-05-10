package com.storage.cameras.rest;

import com.storage.cameras.exception.BadRequestException;
import com.storage.cameras.exception.UnprocessableCameraException;
import com.storage.cameras.rest.resource.ErrorMessage;
import javassist.NotFoundException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import static org.springframework.http.HttpStatus.BAD_REQUEST;
import static org.springframework.http.HttpStatus.NOT_FOUND;
import static org.springframework.http.HttpStatus.UNPROCESSABLE_ENTITY;
import static org.springframework.http.ResponseEntity.status;

@RestControllerAdvice
public class RestServiceExceptionHandler {

    @ExceptionHandler(NotFoundException.class)
    public ResponseEntity handleNotFoundException(final NotFoundException ex) {
        return responseMessage(NOT_FOUND, new ErrorMessage(ex.getMessage()));
    }

    @ExceptionHandler(BadRequestException.class)
    public ResponseEntity handleBadRequestException(final BadRequestException ex) {
        return responseMessage(BAD_REQUEST, new ErrorMessage(ex.getMessage()));
    }

    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ResponseEntity handleMessageNotReadableException(final HttpMessageNotReadableException ex) {
        return responseMessage(BAD_REQUEST,
                new ErrorMessage("Either the request body is missing or its JSON is incorrect"));
    }

    @ExceptionHandler(UnprocessableCameraException.class)
    public ResponseEntity handleUnprocessableCameraException(final UnprocessableCameraException ex) {
        return responseMessage(UNPROCESSABLE_ENTITY,
                new ErrorMessage("The service was unable to communicate with the camera"));
    }

    private static ResponseEntity responseMessage(final HttpStatus httpStatus, final Object messageBody) {
        return status(httpStatus).body(messageBody);
    }
}

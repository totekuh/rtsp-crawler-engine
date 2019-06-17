package com.storage.cameras.rest;

import com.storage.cameras.exception.BadRequestException;
import com.storage.cameras.model.CameraStatus;
import com.storage.cameras.rest.params.SearchCameraParams;

import static java.lang.String.format;
import static java.util.Arrays.asList;
import static org.apache.commons.lang3.StringUtils.isBlank;
import static org.apache.commons.lang3.StringUtils.isNotBlank;

public class SearchCameraParamsValidator {
    private final SearchCameraParams params;

    public SearchCameraParamsValidator(final SearchCameraParams params) {
        this.params = params;
    }

    public void validate() {
        if (isBlank(params.getStatus())) {
            throw new BadRequestException("Missing 'status' parameter in a json body");
        }
        try {
            CameraStatus.valueOf(params.getStatus());
        } catch (IllegalArgumentException e) {
            throw new BadRequestException(format("Illegal 'status' value. " +
                    "Should be one of the following: %s", asList(CameraStatus.values())));
        }
        if (isNotBlank(params.getCountryCode()) && params.getCountryCode().length() != 2) {
            throw new BadRequestException(format("Illegal 'countryCode' value. It should have a length of 2 chars"));
        }
    }
}

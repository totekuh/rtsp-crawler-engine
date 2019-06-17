package com.storage.cameras.rest.params;

import lombok.AllArgsConstructor;
import lombok.Getter;

import javax.validation.constraints.Size;

@Getter
@AllArgsConstructor
public class SearchCameraParams {
    @Size(min = 1, max = 20)
    private String status;

    @Size(max = 2)
    private String countryCode;

}

package com.storage.cameras.rest.params;

import lombok.AllArgsConstructor;
import lombok.Getter;

import javax.validation.constraints.Size;
import java.util.List;
import java.util.Set;

@Getter
@AllArgsConstructor
public class SearchCameraParams {
    @Size(min = 1, max = 20)
    private String status;

    @Size(max = 2)
    private String countryCode;

    @Size(max = 30)
    private String city;

    private Set<String> keywords;

}

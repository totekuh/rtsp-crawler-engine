package com.storage.cameras.rest.params;

import lombok.AllArgsConstructor;
import lombok.Getter;

import javax.validation.constraints.Size;
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

    private Order order;

    public enum Order {
        ID_ASC,
        ID_DESC,
        CREATION_TIMESTAMP_ASC,
        CREATION_TIMESTAMP_DESC;
    }

}

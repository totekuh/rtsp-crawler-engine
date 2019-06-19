package com.storage.cameras.rest.params;

import java.util.Set;
import javax.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class SearchCameraParams {
    @Size(min = 1, max = 20)
    private final String status;

    @Size(max = 2)
    private final String countryCode;

    @Size(max = 30)
    private final String city;

    private final Set<String> keywords;

    private final Order order;

    public enum Order {
        ID_ASC, ID_DESC, CREATION_TIMESTAMP_ASC, CREATION_TIMESTAMP_DESC
    }

}

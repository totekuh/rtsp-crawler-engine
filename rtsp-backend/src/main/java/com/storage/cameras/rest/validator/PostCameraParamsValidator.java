package com.storage.cameras.rest.validator;

import com.storage.cameras.exception.BadRequestException;
import com.storage.cameras.model.Keyword;
import com.storage.cameras.rest.params.PostCameraParams;
import lombok.AllArgsConstructor;
import static java.lang.String.format;
import static java.util.Arrays.asList;
import static org.apache.commons.collections4.CollectionUtils.isNotEmpty;
import static org.apache.commons.lang3.StringUtils.isBlank;
import static org.apache.commons.lang3.StringUtils.isNotBlank;

@AllArgsConstructor
public class PostCameraParamsValidator {
    private final PostCameraParams params;

    public void validate() {
        if (isNotEmpty(params.getKeywords())) {
            try {
                for (final String k : params.getKeywords()) {
                    Keyword.valueOf(k);
                }
            } catch (final IllegalArgumentException ex) {
                throw new BadRequestException(format("Invalid keyword value. Should be one of the following: %s",
                        asList(Keyword.values())));
            }
        }

        final String countryCode = params.getCountryCode();
        if (isNotBlank(countryCode) && countryCode.length() != 2) {
            throw new BadRequestException(format("Field 'countryCode' is invalid. " +
                    "The field value should have only 2 characters length. " +
                    "The actual value is: %s", countryCode));
        }
        
        if (isBlank(params.getUrl())) {
            throw new BadRequestException("Field 'url' cannot be blank");
        }
    }
}

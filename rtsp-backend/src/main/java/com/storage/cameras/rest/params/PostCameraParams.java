package com.storage.cameras.rest.params;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.storage.cameras.model.CameraStatus;
import lombok.Data;
import org.springframework.lang.NonNull;

import javax.validation.constraints.Size;

import static com.storage.cameras.model.Camera.MAX_COMMENT_LENGTH;

@Data
public class PostCameraParams {

    @NonNull
    @JsonProperty("@timestamp")
    private String timestamp;

    private CameraStatus status;

    @Size(max = MAX_COMMENT_LENGTH)
    private String comment;

    private String url;

    private String city;

    private String countryCode;

    private String countryName;

    private String isp;
}

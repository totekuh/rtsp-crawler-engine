package com.storage.cameras.rest;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.storage.cameras.model.CameraStatus;
import lombok.Data;
import org.springframework.lang.NonNull;

@Data
public class PostCameraParams {

    @NonNull
    @JsonProperty("@timestamp")
    private String timestamp;

    private CameraStatus status;

    private String url;

    private String city;

    private String countryCode;

    private String countryName;

    private String isp;
}

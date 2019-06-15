package com.storage.cameras.rest.resource;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class CameraResource {

    private final Long cameraId;

    private final String rtspUrl;

    private String creationTimestamp;

    private String lastUpdateTimestamp;

    private final String status;

    private final String countryName;

    private final String city;

}

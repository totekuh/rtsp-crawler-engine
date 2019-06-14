package com.storage.cameras.rest;

import com.storage.cameras.model.Camera;

import static com.storage.cameras.util.DateTimeUtil.formatDate;

public interface CameraToResourceMapper {
    CameraToResourceMapper INSTANCE = camera -> new CameraResource(
            camera.getId(),
            camera.getUrl(),
            formatDate(camera.getCreationTimestamp()),
            formatDate(camera.getUpdateTimestamp()),
            camera.getStatus().name(),
            camera.getCountryName(),
            camera.getCity()
    );

    CameraResource convert(Camera camera);
}

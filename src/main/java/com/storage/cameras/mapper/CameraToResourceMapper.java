package com.storage.cameras.mapper;

import com.storage.cameras.model.Camera;
import com.storage.cameras.rest.resource.CameraResource;

import static com.storage.cameras.util.DateTimeUtil.formatDateToString;

public interface CameraToResourceMapper {
    CameraToResourceMapper INSTANCE = camera -> new CameraResource(
            camera.getId(),
            camera.getUrl(),
            formatDateToString(camera.getCreationTimestamp()),
            formatDateToString(camera.getUpdateTimestamp()),
            camera.getStatus().name(),
            camera.getCountryName(),
            camera.getCity()
    );

    CameraResource convert(Camera camera);
}

package com.storage.cameras.mapper;

import com.storage.cameras.model.Camera;
import com.storage.cameras.rest.resource.CameraResource;
import static com.storage.cameras.util.DateTimeUtil.formatDateToString;
import static java.util.stream.Collectors.toList;
import static org.apache.commons.lang3.BooleanUtils.isTrue;

public interface CameraToResourceMapper {
    CameraToResourceMapper INSTANCE = camera -> new CameraResource(
            camera.getId(),
            camera.getUrl(),
            camera.getComments()
                    .stream()
                    .map(CommentToResourceMapper.INSTANCE::convert)
                    .collect(toList()),
            formatDateToString(camera.getCreationTimestamp()),
            formatDateToString(camera.getUpdateTimestamp()),
            camera.getStatus().name(),
            camera.getCountryName(),
            camera.getCountryCode(),
            camera.getCity(),
            camera.getKeywords(),
            camera.getBase64ImageData(),
            null);

    CameraResource convert(Camera camera);

    default CameraResource convert(Camera camera, Boolean includeBase64ImageData) {
        final CameraResource cameraResource = INSTANCE.convert(camera);
        if (isTrue(includeBase64ImageData)) {
            // do nothing
        } else {
            cameraResource.setBase64ImageData(null);
        }
        return cameraResource;
    }
}

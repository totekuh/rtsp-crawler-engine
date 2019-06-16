package com.storage.cameras.mapper;

import com.storage.cameras.model.Camera;
import com.storage.cameras.rest.params.PostCameraParams;

import java.util.Date;

import static com.storage.cameras.util.DateTimeUtil.formatStringWithDate;

public interface PostCameraParamsToCameraMapper {
    PostCameraParamsToCameraMapper INSTANCE = new PostCameraParamsToCameraMapper() {
        @Override
        public Camera toNewCamera(final PostCameraParams params) {
            final Camera newCamera = new Camera();
            newCamera.setCreationTimestamp(formatStringWithDate(params.getTimestamp()));
            newCamera.setStatus(params.getStatus());
            newCamera.setUrl(params.getUrl());
            newCamera.setCity(params.getCity());
            newCamera.setCountryCode(params.getCountryCode());
            newCamera.setCountryName(params.getCountryName());
            newCamera.setIsp(params.getIsp());
            newCamera.setComment(params.getComment());
            return newCamera;
        }

        @Override
        public Camera toUpdatedCamera(final Camera camera, final PostCameraParams params) {
            camera.setStatus(params.getStatus());
            camera.setIsp(params.getIsp());
            camera.setCountryCode(params.getCountryCode());
            camera.setCountryName(params.getCountryName());
            camera.setCity(params.getCity());
            camera.setUpdateTimestamp(new Date());
            camera.setComment(params.getComment());
            return camera;
        }
    };

    Camera toNewCamera(PostCameraParams params);

    Camera toUpdatedCamera(Camera camera, PostCameraParams params);
}

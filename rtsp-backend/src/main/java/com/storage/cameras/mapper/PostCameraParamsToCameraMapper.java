package com.storage.cameras.mapper;

import com.storage.cameras.model.Camera;
import com.storage.cameras.rest.params.PostCameraParams;

import java.util.Date;

import static org.apache.commons.lang3.StringUtils.isNotBlank;

public interface PostCameraParamsToCameraMapper {
    PostCameraParamsToCameraMapper INSTANCE = new PostCameraParamsToCameraMapper() {
        @Override
        public Camera toNewCamera(final PostCameraParams params) {
            final Camera newCamera = new Camera();
            newCamera.setCreationTimestamp(new Date());
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
            if (params.getStatus() != null) {
                camera.setStatus(params.getStatus());
            }
            if (isNotBlank(params.getIsp())) {
                camera.setIsp(params.getIsp());
            }
            if (isNotBlank(params.getCountryCode())) {
                camera.setCountryCode(params.getCountryCode());
            }
            if (isNotBlank(params.getCountryName())) {
                camera.setCountryCode(params.getCountryName());
            }
            if (isNotBlank(params.getCity())) {
                camera.setCountryCode(params.getCity());
            }
            camera.setUpdateTimestamp(new Date());
            if (isNotBlank(params.getComment())) {
                camera.setComment(params.getComment());
            }
            return camera;
        }
    };

    Camera toNewCamera(PostCameraParams params);

    Camera toUpdatedCamera(Camera camera, PostCameraParams params);
}
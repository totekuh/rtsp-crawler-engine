package com.storage.cameras.dao;

import com.storage.cameras.model.Camera;
import com.storage.cameras.rest.PostCameraParams;

import java.util.Optional;

public interface CameraDao {
    Camera updateOrCreateCamera(PostCameraParams params);

    Optional<Camera> get(Long id);

    Optional<Camera> getByUrl(String url);
}

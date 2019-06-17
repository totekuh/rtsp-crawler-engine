package com.storage.cameras.dao;

import com.storage.cameras.model.Camera;
import com.storage.cameras.rest.params.PostCameraParams;
import com.storage.cameras.rest.params.SearchCameraParams;

import java.util.List;
import java.util.Optional;

public interface CameraDao {
    Camera updateOrCreateCamera(PostCameraParams params);

    Optional<Camera> get(Long id);

    Optional<Camera> getByUrl(String url);

    List<Camera> search(SearchCameraParams params);

    List<Camera> getAll();
}

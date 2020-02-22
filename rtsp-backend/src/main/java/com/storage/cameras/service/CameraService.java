package com.storage.cameras.service;

import com.storage.cameras.model.Camera;
import com.storage.cameras.rest.params.PostCameraParams;
import com.storage.cameras.rest.params.SearchCameraParams;
import com.storage.cameras.rest.resource.CameraIdentifiersResource;
import com.storage.cameras.rest.resource.CameraResource;
import java.util.List;
import javassist.NotFoundException;

public interface CameraService {

    Camera save(PostCameraParams params);

    Camera get(Long id) throws NotFoundException;

    Camera get(String rtspUrl) throws NotFoundException;

    List<Camera> search(SearchCameraParams params);

    List<Camera> getAll();
    
    List<Long> getCameraIds();

    List<Camera> getWithNoGeolocation();
    
    List<Camera> getAllUnconnected();

    void save(Camera camera);

    void save(List<Camera> cameras);

    void delete(Long id);
}

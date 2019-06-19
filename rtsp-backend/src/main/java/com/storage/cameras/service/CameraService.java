package com.storage.cameras.service;

import com.storage.cameras.rest.params.PostCameraParams;
import com.storage.cameras.rest.params.SearchCameraParams;
import com.storage.cameras.rest.resource.CameraResource;
import java.util.List;
import javassist.NotFoundException;

public interface CameraService {

    CameraResource save(PostCameraParams params);

    CameraResource get(Long id) throws NotFoundException;

    CameraResource get(String rtspUrl) throws NotFoundException;

    List<CameraResource> search(SearchCameraParams params);

    List<CameraResource> getAll();
}

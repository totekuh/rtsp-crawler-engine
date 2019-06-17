package com.storage.cameras.service;

import com.storage.cameras.rest.resource.CameraResource;
import com.storage.cameras.rest.PostCameraParams;
import javassist.NotFoundException;

public interface CameraService {

    CameraResource save(PostCameraParams params);

    CameraResource get(Long id) throws NotFoundException;

    CameraResource get(String rtspUrl) throws NotFoundException;
}

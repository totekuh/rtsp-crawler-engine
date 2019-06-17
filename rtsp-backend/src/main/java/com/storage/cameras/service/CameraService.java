package com.storage.cameras.service;

import com.storage.cameras.rest.resource.CameraResource;
import com.storage.cameras.rest.params.PostCameraParams;
import com.storage.cameras.rest.params.SearchCameraParams;
import javassist.NotFoundException;
import org.springframework.http.ResponseEntity;

import java.util.List;

public interface CameraService {

    CameraResource save(PostCameraParams params);

    CameraResource get(Long id) throws NotFoundException;

    CameraResource get(String rtspUrl) throws NotFoundException;

    List<CameraResource> search(SearchCameraParams params);

    List<CameraResource> getAll();
}

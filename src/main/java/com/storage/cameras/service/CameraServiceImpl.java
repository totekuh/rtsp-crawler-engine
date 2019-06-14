package com.storage.cameras.service;

import com.storage.cameras.dao.CameraDao;
import com.storage.cameras.model.Camera;
import com.storage.cameras.rest.CameraResource;
import com.storage.cameras.rest.CameraToResourceMapper;
import com.storage.cameras.rest.PostCameraParams;
import javassist.NotFoundException;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import static java.lang.String.format;

@Service
@AllArgsConstructor
@Slf4j
public class CameraServiceImpl implements CameraService {
    private final CameraDao cameraDao;
    private final CameraToResourceMapper mapper = CameraToResourceMapper.INSTANCE;

    @Override
    @Transactional
    public CameraResource save(final PostCameraParams params) {
        final Camera camera = cameraDao.updateOrCreateCamera(params);
        return mapper.convert(camera);
    }

    @Override
    @Transactional
    public CameraResource get(final Long id) throws NotFoundException {
        return cameraDao.get(id)
                .map(mapper::convert)
                .orElseThrow(() -> new NotFoundException(format("Camera with id %s was not found.", id)));
    }

    @Override
    @Transactional
    public CameraResource get(final String rtspUrl) throws NotFoundException {
        return cameraDao.getByUrl(rtspUrl)
                .map(mapper::convert)
                .orElseThrow(() -> new NotFoundException(format("Camera with url %s was not found.", rtspUrl)));
    }
}

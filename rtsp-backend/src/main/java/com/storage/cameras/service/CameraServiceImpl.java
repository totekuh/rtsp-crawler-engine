package com.storage.cameras.service;

import com.storage.cameras.dao.CameraDao;
import com.storage.cameras.dao.CommentDao;
import com.storage.cameras.mapper.CameraToResourceMapper;
import com.storage.cameras.model.Camera;
import com.storage.cameras.model.Comment;
import com.storage.cameras.model.Label;
import com.storage.cameras.rest.params.LabelParams;
import com.storage.cameras.rest.params.PostCameraParams;
import com.storage.cameras.rest.params.SearchCameraParams;
import com.storage.cameras.rest.resource.CameraResource;
import java.util.List;
import javassist.NotFoundException;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import static org.apache.commons.collections4.CollectionUtils.isNotEmpty;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import static java.lang.String.format;
import static java.util.stream.Collectors.toList;
import static org.apache.commons.lang3.StringUtils.isNotBlank;
import static org.springframework.transaction.annotation.Propagation.REQUIRED;

@Service
@AllArgsConstructor
@Slf4j
@Transactional(propagation = REQUIRED)
public class CameraServiceImpl implements CameraService {
    private final CameraDao cameraDao;
    private final CommentDao commentDao;
    private final LabelService labelService;
    private final CameraToResourceMapper mapper = CameraToResourceMapper.INSTANCE;

    @Override
    public CameraResource save(final PostCameraParams params) {
        final Camera camera = cameraDao.updateOrCreateCamera(params);
        if (isNotBlank(params.getComment())) {
            final Comment comment = new Comment();
            comment.setComment(params.getComment());
            camera.getComments().add(comment);
            comment.setCamera(camera);
            commentDao.save(comment);
        }
        final List<LabelParams> labelParams = params.getLabels();
        if (isNotEmpty(params.getLabels())) {
            labelParams.forEach(receivedLabel -> {
                final Label label = labelService.findOrCreateLabel(receivedLabel);
                log.info("Adding {} label to the camera with URL: {}", label.getName(), camera.getUrl());
                camera.getLabels().add(label);
            });
        }
        return mapper.convert(camera);
    }

    @Override
    public CameraResource get(final Long id) throws NotFoundException {
        return cameraDao.get(id)
                .map(mapper::convert)
                .orElseThrow(() -> new NotFoundException(format("Camera with id %s was not found.", id)));
    }

    @Override
    public CameraResource get(final String rtspUrl) throws NotFoundException {
        return cameraDao.getByUrl(rtspUrl)
                .map(mapper::convert)
                .orElseThrow(() -> new NotFoundException(format("Camera with url %s was not found.", rtspUrl)));
    }

    @Override
    public List<CameraResource> search(final SearchCameraParams params) {
        return cameraDao.search(params)
                .stream()
                .map(mapper::convert)
                .collect(toList());
    }

    @Override
    public List<CameraResource> getAll() {
        return cameraDao.getAll()
                .stream()
                .map(mapper::convert)
                .collect(toList());
    }

    @Override
    public List<Long> getCameraIds() {
        return cameraDao.getAllIds();
    }

    @Override
    public List<Camera> getWithNoGeolocation() {
        return cameraDao.findWithNoGeolocation();
    }

    @Override
    public List<Camera> getAllUnconnected() {
        return cameraDao.getAllUnconnected();
    }

    @Override
    public void save(final Camera camera) {
        cameraDao.save(camera);
    }

    @Override
    public void save(final List<Camera> cameras) {
        cameraDao.save(cameras);
    }

    @Override
    public void delete(Long id) {
        cameraDao.delete(id);
    }
}

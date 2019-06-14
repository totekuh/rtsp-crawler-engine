package com.storage.cameras.dao;

import com.storage.cameras.model.Camera;
import com.storage.cameras.model.CameraStatus;
import com.storage.cameras.rest.PostCameraParams;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import java.util.Date;
import java.util.Optional;

import static com.storage.cameras.util.DateTimeUtil.formatString;
import static java.util.Optional.empty;
import static org.springframework.transaction.annotation.Propagation.MANDATORY;

@Slf4j
@Repository
@AllArgsConstructor
public class CameraDaoImpl implements CameraDao {
    private final DataJpaCameraRepository dataJpaCameraRepository;

    @Override
    @Transactional(propagation = MANDATORY)
    public Camera updateOrCreateCamera(final PostCameraParams params) {
        return getByUrl(params.getUrl())
                .map(camera -> {
                    camera.setStatus(params.getStatus());
                    camera.setIsp(params.getIsp());
                    camera.setCountryCode(params.getCountryCode());
                    camera.setCountryName(params.getCountryName());
                    camera.setCity(params.getCity());
                    camera.setUpdateTimestamp(new Date());
                    return dataJpaCameraRepository.save(camera);
                })
                .orElseGet(() -> {
                    final Camera newCamera = new Camera();
                    newCamera.setCreationTimestamp(formatString(params.getTimestamp()));
                    newCamera.setStatus(params.getStatus());
                    newCamera.setUrl(params.getUrl());
                    newCamera.setCity(params.getCity());
                    newCamera.setCountryCode(params.getCountryCode());
                    newCamera.setCountryName(params.getCountryName());
                    newCamera.setIsp(params.getIsp());
                    return dataJpaCameraRepository.save(newCamera);
                });
    }

    @Override
    public Optional<Camera> get(final Long id) {
        try {
            return Optional.ofNullable(dataJpaCameraRepository.getById(id));
        } catch (final Exception e) {
            log.error("Unexpected error: ", e);
            return empty();
        }
    }

    @Override
    public Optional<Camera> getByUrl(final String url) {
        try {
            return Optional.ofNullable(dataJpaCameraRepository.getByUrl(url));
        } catch (final Exception e) {
            log.error("Unexpected error: ", e);
            return empty();
        }
    }
}

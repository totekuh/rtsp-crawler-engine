package com.storage.cameras.dao;

import com.storage.cameras.mapper.PostCameraParamsToCameraMapper;
import com.storage.cameras.model.Camera;
import com.storage.cameras.rest.PostCameraParams;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

import static com.storage.cameras.mapper.PostCameraParamsToCameraMapper.INSTANCE;
import static java.util.Optional.empty;
import static org.springframework.transaction.annotation.Propagation.MANDATORY;

@Slf4j
@Repository
@AllArgsConstructor
public class CameraDaoImpl implements CameraDao {
    private final DataJpaCameraRepository dataJpaCameraRepository;
    private static final PostCameraParamsToCameraMapper mapper = INSTANCE;

    @Override
    @Transactional(propagation = MANDATORY)
    public Camera updateOrCreateCamera(final PostCameraParams params) {
        return getByUrl(params.getUrl())
                .map(camera -> dataJpaCameraRepository.save(mapper.toUpdatedCamera(camera, params)))
                .orElseGet(() -> dataJpaCameraRepository.save(mapper.toNewCamera(params)));
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

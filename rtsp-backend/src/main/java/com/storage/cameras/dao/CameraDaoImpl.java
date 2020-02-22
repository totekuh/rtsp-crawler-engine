package com.storage.cameras.dao;

import com.storage.cameras.mapper.PostCameraParamsToCameraMapper;
import static com.storage.cameras.mapper.PostCameraParamsToCameraMapper.INSTANCE;
import com.storage.cameras.model.Camera;
import com.storage.cameras.model.CameraStatus;
import static com.storage.cameras.model.CameraStatus.UNCONNECTED;
import com.storage.cameras.model.Keyword;
import com.storage.cameras.rest.params.PostCameraParams;
import com.storage.cameras.rest.params.SearchCameraParams;
import static com.storage.cameras.rest.params.SearchCameraParams.Order.CREATION_TIMESTAMP_ASC;
import static com.storage.cameras.rest.params.SearchCameraParams.Order.CREATION_TIMESTAMP_DESC;
import static com.storage.cameras.rest.params.SearchCameraParams.Order.ID_ASC;
import static com.storage.cameras.rest.params.SearchCameraParams.Order.ID_DESC;
import static java.util.Comparator.comparing;
import java.util.List;
import java.util.Optional;
import static java.util.Optional.empty;
import static java.util.stream.Collectors.toList;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import static org.apache.commons.collections4.CollectionUtils.isNotEmpty;
import static org.apache.commons.lang3.StringUtils.isNotBlank;
import org.springframework.stereotype.Repository;
import static org.springframework.transaction.annotation.Propagation.MANDATORY;
import org.springframework.transaction.annotation.Transactional;

@Slf4j
@Repository
@AllArgsConstructor
@Transactional(propagation = MANDATORY)
public class CameraDaoImpl implements CameraDao {
    private final DataJpaCameraRepository dataJpaCameraRepository;
    private static final PostCameraParamsToCameraMapper mapper = INSTANCE;

    @Override
    public Camera updateOrCreateCamera(final PostCameraParams params) {
        return getByUrl(params.getUrl())
                .map(c -> dataJpaCameraRepository.save(mapper.toUpdatedCamera(c, params)))
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

    @Override
    public List<Camera> search(final SearchCameraParams params) {
        final CameraStatus status = CameraStatus.valueOf(params.getStatus());
        final String countryCode = params.getCountryCode();
        final String city = params.getCity();

        final List<Camera> cameras;
        if (isNotBlank(countryCode)) {
            cameras = dataJpaCameraRepository.findAllByStatusAndCountryCode(status, countryCode);
        } else if (isNotBlank(city)) {
            cameras = dataJpaCameraRepository.findAllByStatusAndCity(status, city);
        } else {
            cameras = dataJpaCameraRepository.findAllByStatus(status);
        }
        if (isNotEmpty(params.getKeywords())) {
            return cameras
                    .stream()
                    .filter(camera -> {
                        for (final String keyword : params.getKeywords()) {
                            return camera.getKeywords().contains(Keyword.valueOf(keyword));
                        }
                        return false;
                    })
                    .collect(toList());
        }

        if (params.getOrder() != null) {
            final SearchCameraParams.Order order = params.getOrder();
            if (order == CREATION_TIMESTAMP_ASC) {
                return cameras
                        .stream()
                        .sorted(comparing(Camera::getCreationTimestamp))
                        .collect(toList());
            } else if (order == CREATION_TIMESTAMP_DESC) {
                return cameras
                        .stream()
                        .sorted(comparing(Camera::getCreationTimestamp).reversed())
                        .collect(toList());
            } else if (order == ID_ASC) {
                return cameras
                        .stream()
                        .sorted(comparing(Camera::getId))
                        .collect(toList());
            } else if (order == ID_DESC) {
                return cameras
                        .stream()
                        .sorted(comparing(Camera::getId).reversed())
                        .collect(toList());
            }

        }
        return cameras;
    }

    @Override
    public List<Camera> getAll() {
        return dataJpaCameraRepository.findAll();
    }

    @Override
    public void save(final Camera camera) {
        dataJpaCameraRepository.save(camera);
    }

    @Override
    public void save(final List<Camera> cameras) {
        dataJpaCameraRepository.saveAll(cameras);
    }

    @Override
    public List<Camera> findWithNoGeolocation() {
        return dataJpaCameraRepository.findWithNoGeolocation();
    }

    @Override
    public List<Long> getAllIds() {
        return dataJpaCameraRepository.getAllIds();
    }

    @Override
    public List<Camera> getAllUnconnected() {
        return dataJpaCameraRepository.findAllByStatus(UNCONNECTED);
    }

    @Override
    public void delete(Long id) {
        dataJpaCameraRepository.deleteById(id);
    }
}

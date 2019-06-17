package com.storage.cameras.dao;

import com.storage.cameras.exception.BadRequestException;
import com.storage.cameras.mapper.PostCameraParamsToCameraMapper;
import com.storage.cameras.model.Camera;
import com.storage.cameras.model.CameraStatus;
import com.storage.cameras.model.Comment;
import com.storage.cameras.rest.params.PostCameraParams;
import com.storage.cameras.rest.params.SearchCameraParams;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import static com.storage.cameras.mapper.PostCameraParamsToCameraMapper.INSTANCE;
import static java.lang.String.format;
import static java.util.Optional.empty;
import static org.apache.commons.lang3.StringUtils.isNotBlank;
import static org.springframework.transaction.annotation.Propagation.MANDATORY;

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
    public List<Camera> search(SearchCameraParams params) {
        final CameraStatus status = CameraStatus.valueOf(params.getStatus());
        final String countryCode = params.getCountryCode();
        final String city = params.getCity();

        if (isNotBlank(countryCode)) {
            return dataJpaCameraRepository.findAllByStatusAndCountryCode(status, countryCode);
        }
        if (isNotBlank(city)) {
            return dataJpaCameraRepository.findAllByStatusAndCity(status, city);
        }
        return dataJpaCameraRepository.findAllByStatus(status);
    }

    @Override
    public List<Camera> getAll() {
        return dataJpaCameraRepository.findAll();
    }
}

package com.storage.cameras.rest;

import com.storage.cameras.mapper.CameraToResourceMapper;
import com.storage.cameras.mapper.LabelToResourceMapper;
import com.storage.cameras.model.Camera;
import static com.storage.cameras.model.RequestPath.CAMERAS_URL;
import com.storage.cameras.rest.params.PostCameraParams;
import com.storage.cameras.rest.params.SearchCameraParams;
import com.storage.cameras.rest.resource.CameraIdentifiersResource;
import com.storage.cameras.rest.resource.CameraResource;
import com.storage.cameras.rest.resource.CameraResourceContainer;
import com.storage.cameras.rest.validator.PostCameraParamsValidator;
import com.storage.cameras.rest.validator.SearchCameraParamsValidator;
import com.storage.cameras.service.CameraService;
import com.storage.cameras.service.LabelService;
import java.util.List;
import static java.util.stream.Collectors.toList;
import static java.util.stream.Collectors.toSet;
import javax.validation.Valid;
import lombok.AllArgsConstructor;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import static org.apache.commons.lang3.StringUtils.isNotBlank;
import static org.springframework.http.MediaType.APPLICATION_JSON_VALUE;
import org.springframework.http.ResponseEntity;
import static org.springframework.http.ResponseEntity.ok;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping(CAMERAS_URL)
@AllArgsConstructor
@Slf4j
public class CameraRestController {

    private final CameraService cameraService;
    private final LabelService labelService;
    private final CameraToResourceMapper cameraToResourceMapper = CameraToResourceMapper.INSTANCE;
    private final LabelToResourceMapper labelToResourceMapper = LabelToResourceMapper.INSTANCE;

    @PutMapping(value = "/import", consumes = APPLICATION_JSON_VALUE, produces = APPLICATION_JSON_VALUE)
    public ResponseEntity receive(@RequestBody final PostCameraParams params) {
        new PostCameraParamsValidator(params).validate();
        log.info("Import a camera: {}", params.getUrl());
        return ok(cameraService.save(params));
    }

    @SneakyThrows
    @GetMapping(produces = APPLICATION_JSON_VALUE)
    public ResponseEntity get(@RequestParam(required = false) final Long id,
                              @RequestParam(required = false) final String rtspUrl,
                              @RequestParam(required = false) final Boolean includeBase64ImageData) {
        if (id != null || isNotBlank(rtspUrl)) {
            final Camera camera;
            if (id != null) {
                log.info("Get a camera: {}", id);
                camera = cameraService.get(id);
            } else {
                log.info("Get a camera: {}", rtspUrl);
                camera = cameraService.get(rtspUrl);
            }
            final CameraResource cameraResource =
                    cameraToResourceMapper.convert(camera, includeBase64ImageData);
            cameraResource.setLabels(labelService.getLabelsByCamera(camera)
                    .stream()
                    .map(labelToResourceMapper::convert)
                    .collect(toSet()));
            return ok(cameraResource);
        }
        final List<CameraResource> cameras;
        if (includeBase64ImageData) {
            cameras = cameraService.getAll()
                    .stream()
                    .map(cameraToResourceMapper::convert)
                    .collect(toList());
        } else {
            cameras = cameraService.getAll()
                    .stream()
                    .map(camera -> {
                        camera.setBase64ImageData(null);
                        return cameraToResourceMapper.convert(camera);
                    })
                    .collect(toList());
        }

        return ok(new CameraResourceContainer(cameras.size(), cameras));
    }

    @SneakyThrows
    @GetMapping(path = "/ids", produces = APPLICATION_JSON_VALUE)
    public ResponseEntity getCameraIds() {
        log.info("Getting camera ids");
        final List<Long> cameraIds = cameraService.getCameraIds();
        return ok(new CameraIdentifiersResource(cameraIds));
    }

    @SneakyThrows
    @PostMapping(value = "/search", consumes = APPLICATION_JSON_VALUE, produces = APPLICATION_JSON_VALUE)
    public ResponseEntity search(@RequestBody @Valid SearchCameraParams params) {
        new SearchCameraParamsValidator(params).validate();
        final List<CameraResource> cameras = cameraService.search(params)
                .stream()
                .map(cameraToResourceMapper::convert)
                .collect(toList());
        return ok(new CameraResourceContainer(cameras.size(), cameras));
    }
}
